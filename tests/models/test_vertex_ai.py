#!/usr/bin/env python3
"""Test script to verify Vertex AI configuration is working."""

import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_vertex_ai():
    """Test if Vertex AI credentials are properly configured."""

    # Check if project and location are set
    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION")
    use_vertex = os.getenv("GOOGLE_GENAI_USE_VERTEXAI")

    assert project is not None, "GOOGLE_CLOUD_PROJECT not set"
    assert location is not None, "GOOGLE_CLOUD_LOCATION not set"

    print(f"✅ GOOGLE_CLOUD_PROJECT: {project}")
    print(f"✅ GOOGLE_CLOUD_LOCATION: {location}")
    print(f"✅ GOOGLE_GENAI_USE_VERTEXAI: {use_vertex}")

    # Check if ADC credentials exist
    adc_path = os.path.expanduser(
        "~/.config/gcloud/application_default_credentials.json"
    )
    assert os.path.exists(adc_path), "Application Default Credentials not found"
    print("✅ Application Default Credentials found")

    # Try to import and test the client
    from google.genai import Client

    # Create client with Vertex AI configuration
    client = Client(vertexai=True, project=project, location=location)
    print("✅ Vertex AI client created successfully")
    assert client is not None


if __name__ == "__main__":
    print("Testing Vertex AI configuration...")
    if test_vertex_ai():
        print(
            "\n🎉 Vertex AI configuration test passed! "
            "You can now run your agent with Vertex AI."
        )
    else:
        print(
            "\n❌ Vertex AI configuration test failed. "
            "Please check your setup."
        )
