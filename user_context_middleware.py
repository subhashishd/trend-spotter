#!/usr/bin/env python3
"""
User Context Middleware Extension

This middleware extends the authentication system to provide user context
to agents that need access to the logged-in user's information.
"""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from trend_spotter.sub_agents.email_agent import set_current_user_email


class UserContextMiddleware(BaseHTTPMiddleware):
    """
    Middleware to set user context in thread-local storage for use by agents.

    This middleware should be added after the authentication middleware
    so that request.state.user is already populated.
    """

    async def dispatch(self, request: Request, call_next):
        """
        Process the request and set user context if user is authenticated.
        """
        # Check if user is authenticated (set by auth middleware)
        user_info = getattr(request.state, "user", None)

        if user_info and user_info.get("email"):
            # Set the user's email in thread-local storage for the email agent
            set_current_user_email(user_info["email"])

        # Continue with the request
        response = await call_next(request)
        return response


def add_user_context_middleware(app):
    """
    Add the user context middleware to the FastAPI app.

    This should be called after authentication middleware is added.
    """
    app.add_middleware(UserContextMiddleware)
    return app
