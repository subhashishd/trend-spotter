#!/usr/bin/env python3
"""Test script to verify API credentials are working."""

import os

import pytest
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_credentials():
    """Test if credentials are properly configured."""

    # Check if API key is set
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("❌ GOOGLE_API_KEY not set or still using placeholder")
        print("Please update your .env file with your actual API key")
        pytest.skip("GOOGLE_API_KEY not configured")

    print(f"✅ GOOGLE_API_KEY is set (ends with: ...{api_key[-4:]})")

    # Check optional Google Search credentials
    search_api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
    search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

    if search_api_key and search_engine_id:
        print("✅ Google Search API credentials are set")
    else:
        print(
            "⚠️  Google Search API credentials not set "
            "(google_search tool won't work)"
        )

    # Try to import and test the client
    from google.genai import Client

    client = Client(api_key=api_key)
    print("✅ Google GenAI client created successfully")
    assert client is not None


if __name__ == "__main__":
    print("Testing API credentials...")
    if test_credentials():
        print("\n🎉 Credentials test passed! You can now run your agent.")
    else:
        print("\n❌ Credentials test failed. Please check your .env file.")
