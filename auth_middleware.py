#!/usr/bin/env python3
"""
Google OAuth2 Authentication Middleware for ADK FastAPI Application

This middleware provides Google Sign-In authentication for the ADK web interface.
Users who are not authenticated will be redirected to Google Sign-In.
"""

import json
import os
from typing import Optional

from authlib.integrations.starlette_client import OAuth
from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse
from google.auth.transport import requests
from google.oauth2 import id_token
from starlette.middleware.base import BaseHTTPMiddleware


class GoogleOAuth2Middleware(BaseHTTPMiddleware):
    """
    Middleware to handle Google OAuth2 authentication for ADK web interface.

    This middleware:
    1. Checks if user is authenticated via session cookie
    2. Redirects unauthenticated users to Google Sign-In
    3. Handles OAuth2 callback and validates tokens
    4. Sets session cookies for authenticated users
    """

    def __init__(self, app, client_id: str, client_secret: str, redirect_uri: str):
        super().__init__(app)
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

        # Initialize OAuth client
        self.oauth = OAuth()
        self.oauth.register(
            name="google",
            client_id=client_id,
            client_secret=client_secret,
            server_metadata_url=(
                "https://accounts.google.com/.well-known/openid-configuration"
            ),
            client_kwargs={"scope": "openid email profile"},
        )

        # Paths that don't require authentication
        self.public_paths = {
            "/auth/login",
            "/auth/callback",
            "/auth/logout",
            "/health",
            "/docs",
            "/redoc",
            "/openapi.json",
        }

    async def dispatch(self, request: Request, call_next):
        """
        Process the request through the authentication middleware.
        """
        path = request.url.path

        # Handle authentication routes first (these are always public)
        if path == "/auth/login":
            return await self._handle_login(request)
        elif path == "/auth/callback":
            return await self._handle_callback(request)
        elif path == "/auth/logout":
            return await self._handle_logout(request)

        # Allow other public paths without authentication
        if any(path.startswith(public_path) for public_path in self.public_paths):
            return await call_next(request)

        # For all other paths (including root /), check authentication
        user_info = await self._get_user_from_session(request)
        if not user_info:
            # Redirect to login
            login_url = f"/auth/login?next={request.url.path}"
            return RedirectResponse(url=login_url, status_code=302)

        # Add user info to request state
        request.state.user = user_info

        # Continue with the request
        response = await call_next(request)
        return response

    async def _handle_login(self, request: Request) -> RedirectResponse:
        """
        Initiate Google OAuth2 login flow.
        """
        next_url = request.query_params.get("next", "/")

        # Build authorization URL manually to avoid session dependency
        from urllib.parse import urlencode

        state = next_url  # Store the next URL in state

        # Google OAuth2 authorization URL
        auth_params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "openid email profile",
            "response_type": "code",
            "state": state,
            "access_type": "offline",
            "prompt": "consent",
        }

        auth_url = f"https://accounts.google.com/o/oauth2/auth?{urlencode(auth_params)}"
        return RedirectResponse(url=auth_url, status_code=302)

    async def _handle_callback(self, request: Request) -> RedirectResponse:
        """
        Handle Google OAuth2 callback and validate the token.
        """
        try:
            # Get the authorization code from callback
            code = request.query_params.get("code")
            if not code:
                raise HTTPException(
                    status_code=400, detail="No authorization code provided"
                )

            # Exchange code for tokens using direct HTTP request
            import httpx

            token_data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": self.redirect_uri,
            }

            async with httpx.AsyncClient() as client:
                token_response = await client.post(
                    "https://oauth2.googleapis.com/token", data=token_data
                )
                token_response.raise_for_status()
                token_json = token_response.json()

            # Verify the ID token
            id_info = id_token.verify_oauth2_token(
                token_json["id_token"], requests.Request(), self.client_id
            )

            # Extract user information
            user_info = {
                "email": id_info.get("email"),
                "name": id_info.get("name"),
                "picture": id_info.get("picture"),
                "sub": id_info.get("sub"),
                "verified_email": id_info.get("email_verified", False),
            }

            # Check if email is verified
            if not user_info["verified_email"]:
                raise HTTPException(
                    status_code=403, detail="Email not verified with Google"
                )

            # Create session
            session_data = json.dumps(user_info)

            # Get next URL from state
            next_url = request.query_params.get("state", "/")

            # Create response with session cookie
            response = RedirectResponse(url=next_url, status_code=302)
            response.set_cookie(
                key="auth_session",
                value=session_data,
                httponly=True,
                secure=False,  # Set to False for local development
                samesite="lax",
                max_age=3600 * 24,  # 24 hours
            )

            return response

        except Exception as e:
            print(f"Authentication error: {e}")
            raise HTTPException(status_code=401, detail="Authentication failed")

    async def _handle_logout(self, request: Request) -> RedirectResponse:
        """
        Handle user logout.
        """
        response = RedirectResponse(url="/", status_code=302)
        response.delete_cookie("auth_session")
        return response

    async def _get_user_from_session(self, request: Request) -> Optional[dict]:
        """
        Get user information from session cookie.
        """
        try:
            session_cookie = request.cookies.get("auth_session")
            if not session_cookie:
                return None

            user_info = json.loads(session_cookie)
            return user_info

        except (json.JSONDecodeError, KeyError):
            return None


def create_auth_middleware(app):
    """
    Factory function to create and configure the OAuth2 middleware.
    """
    # Get OAuth2 configuration from environment
    client_id = os.getenv("GOOGLE_OAUTH2_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_OAUTH2_CLIENT_SECRET")

    if not client_id or not client_secret:
        print("⚠️  Google OAuth2 credentials not found in environment variables.")
        print("   Set GOOGLE_OAUTH2_CLIENT_ID and GOOGLE_OAUTH2_CLIENT_SECRET")
        print("   Skipping authentication middleware.")
        return app

    # Determine redirect URI based on environment
    base_url = os.getenv("GOOGLE_OAUTH2_REDIRECT_BASE_URL", "http://localhost:8080")
    redirect_uri = f"{base_url}/auth/callback"

    print("🔐 Enabling Google OAuth2 authentication")
    print(f"   Client ID: {client_id[:20]}...")
    print(f"   Redirect URI: {redirect_uri}")

    # Add the middleware
    app.add_middleware(
        GoogleOAuth2Middleware,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
    )

    return app
