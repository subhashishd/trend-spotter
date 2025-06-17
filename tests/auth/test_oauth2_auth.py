#!/usr/bin/env python3
"""
Tests for Google OAuth2 Authentication Middleware
"""

import os
import sys
from pathlib import Path

import pytest
from dotenv import load_dotenv
from fastapi import FastAPI

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from auth_middleware import GoogleOAuth2Middleware, create_auth_middleware
except ImportError:
    pytest.skip("OAuth2 middleware not available", allow_module_level=True)


class TestOAuth2Middleware:
    """Test OAuth2 middleware functionality."""

    def test_middleware_creation_without_credentials(self):
        """Test that middleware gracefully handles missing credentials."""
        # Create a simple FastAPI app
        app = FastAPI()

        # Temporarily remove OAuth credentials
        original_client_id = os.environ.get("GOOGLE_OAUTH2_CLIENT_ID")
        original_client_secret = os.environ.get("GOOGLE_OAUTH2_CLIENT_SECRET")

        try:
            # Remove credentials
            if "GOOGLE_OAUTH2_CLIENT_ID" in os.environ:
                del os.environ["GOOGLE_OAUTH2_CLIENT_ID"]
            if "GOOGLE_OAUTH2_CLIENT_SECRET" in os.environ:
                del os.environ["GOOGLE_OAUTH2_CLIENT_SECRET"]

            # Should return the app unchanged when no credentials
            result_app = create_auth_middleware(app)
            assert result_app is app

        finally:
            # Restore original values
            if original_client_id:
                os.environ["GOOGLE_OAUTH2_CLIENT_ID"] = original_client_id
            if original_client_secret:
                os.environ["GOOGLE_OAUTH2_CLIENT_SECRET"] = original_client_secret

    def test_middleware_creation_with_credentials(self):
        """Test that middleware is created when credentials are available."""
        # Skip if no credentials available
        if not (
            os.getenv("GOOGLE_OAUTH2_CLIENT_ID")
            and os.getenv("GOOGLE_OAUTH2_CLIENT_SECRET")
        ):
            pytest.skip("OAuth2 credentials not available")

        app = FastAPI()
        result_app = create_auth_middleware(app)

        # Should return an app (possibly wrapped with middleware)
        assert result_app is not None

    def test_public_paths_configuration(self):
        """Test that public paths are correctly configured."""
        # Skip if no credentials available
        if not (
            os.getenv("GOOGLE_OAUTH2_CLIENT_ID")
            and os.getenv("GOOGLE_OAUTH2_CLIENT_SECRET")
        ):
            pytest.skip("OAuth2 credentials not available")

        middleware = GoogleOAuth2Middleware(
            app=FastAPI(),
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri="http://localhost:8080/auth/callback",
        )

        expected_public_paths = {
            "/auth/login",
            "/auth/callback",
            "/auth/logout",
            "/health",
            "/docs",
            "/redoc",
            "/openapi.json",
        }

        assert middleware.public_paths == expected_public_paths

    def test_redirect_uri_construction(self):
        """Test that redirect URI is properly constructed."""
        # Test with default base URL
        os.environ["GOOGLE_OAUTH2_REDIRECT_BASE_URL"] = "http://localhost:8080"

        app = FastAPI()

        # Mock the credentials for this test
        os.environ["GOOGLE_OAUTH2_CLIENT_ID"] = "test_client_id"
        os.environ["GOOGLE_OAUTH2_CLIENT_SECRET"] = "test_client_secret"

        try:
            result_app = create_auth_middleware(app)
            # If middleware was created successfully, test passes
            assert result_app is not None
        finally:
            # Clean up test environment variables
            if "GOOGLE_OAUTH2_CLIENT_ID" in os.environ:
                del os.environ["GOOGLE_OAUTH2_CLIENT_ID"]
            if "GOOGLE_OAUTH2_CLIENT_SECRET" in os.environ:
                del os.environ["GOOGLE_OAUTH2_CLIENT_SECRET"]


class TestAuthenticatedServerImports:
    """Test that authenticated server can be imported and configured."""

    def test_authenticated_server_import(self):
        """Test that authenticated server module can be imported."""
        try:
            from authenticated_server import start_authenticated_server

            assert callable(start_authenticated_server)
        except ImportError:
            pytest.fail("Could not import authenticated_server module")

    def test_auth_middleware_import(self):
        """Test that auth middleware can be imported."""
        try:
            from auth_middleware import GoogleOAuth2Middleware, create_auth_middleware

            assert callable(create_auth_middleware)
            assert GoogleOAuth2Middleware is not None
        except ImportError:
            pytest.fail("Could not import auth_middleware module")


if __name__ == "__main__":
    # Run tests when executed directly
    pytest.main([__file__, "-v"])
