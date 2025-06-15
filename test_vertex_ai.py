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

    if not project:
        print("❌ GOOGLE_CLOUD_PROJECT not set")
        return False

    if not location:
        print("❌ GOOGLE_CLOUD_LOCATION not set")
        return False

    print(f"✅ GOOGLE_CLOUD_PROJECT: {project}")
    print(f"✅ GOOGLE_CLOUD_LOCATION: {location}")
    print(f"✅ GOOGLE_GENAI_USE_VERTEXAI: {use_vertex}")

    # Check if ADC credentials exist
    adc_path = os.path.expanduser(
        "~/.config/gcloud/application_default_credentials.json"
    )
    if os.path.exists(adc_path):
        print("✅ Application Default Credentials found")
    else:
        print("❌ Application Default Credentials not found")
        return False

    # Try to import and test the client
    try:
        from google.genai import Client

        # Create client with Vertex AI configuration
        _ = Client(vertexai=True, project=project, location=location)
        print("✅ Vertex AI client created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating Vertex AI client: {e}")
        return False


if __name__ == "__main__":
    print("Testing Vertex AI configuration...")
    if test_vertex_ai():
        print(
            "\n🎉 Vertex AI configuration test passed! "
            "You can now run your agent with Vertex AI."
        )
    else:
        print("\n❌ Vertex AI configuration test failed. Please check your setup.")
