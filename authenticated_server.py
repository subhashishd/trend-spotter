#!/usr/bin/env python3
"""
Custom ADK Server with Google OAuth2 Authentication

This script starts the ADK FastAPI server with Google OAuth2 middleware
to provide secure access to the agent interface.
"""

import os
import sys
from pathlib import Path

# Load environment variables from .env file
from dotenv import load_dotenv

load_dotenv()

# Add the current directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

try:
    # Import auth middleware after path setup
    from auth_middleware import create_auth_middleware
    from user_context_middleware import add_user_context_middleware
except ImportError:
    # Fallback if middleware is not available
    def create_auth_middleware(app):
        return app

    def add_user_context_middleware(app):
        return app


def start_authenticated_server(
    agents_dir: str = ".", host: str = "0.0.0.0", port: int = 8080, reload: bool = False
):
    """
    Start the ADK server with Google OAuth2 authentication.
    """
    try:
        # Import ADK modules
        import uvicorn
        from google.adk.cli.fast_api import get_fast_api_app

        print("🚀 Starting ADK server with Google OAuth2 authentication...")
        print(f"   Agents directory: {agents_dir}")
        print(f"   Host: {host}")
        print(f"   Port: {port}")
        print("")

        # Create the ADK FastAPI application
        app = get_fast_api_app(
            agents_dir=agents_dir,
            session_service_uri=os.getenv("SESSION_SERVICE_URI"),
            artifact_service_uri=os.getenv("ARTIFACT_SERVICE_URI"),
            memory_service_uri=os.getenv("MEMORY_SERVICE_URI"),
            allow_origins=(
                os.getenv("ALLOW_ORIGINS", "").split(",")
                if os.getenv("ALLOW_ORIGINS")
                else None
            ),
            web=True,  # Enable web UI
            trace_to_cloud=os.getenv("TRACE_TO_CLOUD", "false").lower() == "true",
        )

        # Add SessionMiddleware required for OAuth2
        # (must be added before auth middleware)
        import secrets

        from starlette.middleware.sessions import SessionMiddleware

        # Get OAuth2 configuration to check if we need authentication
        client_id = os.getenv("GOOGLE_OAUTH2_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_OAUTH2_CLIENT_SECRET")

        if client_id and client_secret:
            # Add session middleware first
            app.add_middleware(
                SessionMiddleware,
                secret_key=os.getenv("SESSION_SECRET_KEY", secrets.token_urlsafe(32)),
            )

            # Then add Google OAuth2 authentication middleware
            app = create_auth_middleware(app)

            # Add user context middleware after authentication
            app = add_user_context_middleware(app)
        else:
            print("⚠️  OAuth2 credentials not found - running without authentication")

        # Add custom authentication status endpoint
        @app.get("/auth/status")
        async def auth_status(request):
            """Get current authentication status."""
            user = getattr(request.state, "user", None)
            if user:
                return {
                    "authenticated": True,
                    "user": {
                        "email": user.get("email"),
                        "name": user.get("name"),
                        "picture": user.get("picture"),
                    },
                }
            return {"authenticated": False}

        print("🌐 Server will be available at:")
        print(f"   - Main app: http://{host}:{port}/")
        print(f"   - API docs: http://{host}:{port}/docs")
        print(f"   - Auth status: http://{host}:{port}/auth/status")
        print(f"   - Logout: http://{host}:{port}/auth/logout")
        print("")

        # Start the server
        uvicorn.run(app, host=host, port=port, reload=reload, log_level="info")

    except ImportError as e:
        print(f"❌ Error importing ADK modules: {e}")
        print("   Make sure google-adk is installed and accessible")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Start ADK server with Google OAuth2 authentication"
    )
    parser.add_argument(
        "agents_dir",
        nargs="?",
        default=".",
        help="Directory containing agent configurations",
    )
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind the server to")
    parser.add_argument(
        "--port", type=int, default=8080, help="Port to bind the server to"
    )
    parser.add_argument(
        "--reload", action="store_true", help="Enable auto-reload for development"
    )

    args = parser.parse_args()

    start_authenticated_server(
        agents_dir=args.agents_dir, host=args.host, port=args.port, reload=args.reload
    )
