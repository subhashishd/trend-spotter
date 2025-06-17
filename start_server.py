#!/usr/bin/env python3
"""
Production Server Entrypoint

This script automatically chooses between authenticated and non-authenticated
ADK server based on available OAuth2 credentials.
"""

import os
import subprocess
import sys
from pathlib import Path

# Load environment variables if .env file exists
try:
    from dotenv import load_dotenv

    if Path(".env").exists():
        load_dotenv()
except ImportError:
    pass  # dotenv not available in production


def main():
    """
    Start ADK server with or without authentication based on available credentials.
    """
    # Check if OAuth2 credentials are available
    client_id = os.getenv("GOOGLE_OAUTH2_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_OAUTH2_CLIENT_SECRET")

    if client_id and client_secret:
        print("🔐 OAuth2 credentials detected - starting authenticated server...")
        try:
            # Try to use authenticated server
            from authenticated_server import start_authenticated_server

            # Pass any command line arguments
            start_authenticated_server(*sys.argv[1:])
        except ImportError:
            print(
                "⚠️  Authenticated server not available, "
                "falling back to standard ADK..."
            )
            # Fall back to standard ADK
            subprocess.run(["adk", "web"] + sys.argv[1:])
    else:
        print("🌐 No OAuth2 credentials found - starting standard ADK server...")
        # Use standard ADK web server
        subprocess.run(["adk", "web"] + sys.argv[1:])


if __name__ == "__main__":
    main()
