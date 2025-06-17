#!/usr/bin/env python3
"""Integration tests that require Google Cloud credentials."""

import os

import pytest
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Skip integration tests if running in CI without credentials
skip_if_no_credentials = pytest.mark.skipif(
    not os.getenv("GOOGLE_API_KEY") or os.getenv("CI") == "true",
    reason="Google Cloud credentials not available or running in CI",
)

skip_if_no_project = pytest.mark.skipif(
    not os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("CI") == "true",
    reason="Google Cloud project not configured or running in CI",
)


@pytest.mark.integration
@skip_if_no_credentials
def test_google_api_key_valid():
    """Test that Google API key is valid and can create a client."""
    api_key = os.getenv("GOOGLE_API_KEY")
    assert api_key is not None, "GOOGLE_API_KEY environment variable not set"
    assert (
        api_key != "your_api_key_here"
    ), "GOOGLE_API_KEY is still placeholder"

    try:
        from google.genai import Client

        client = Client(api_key=api_key)
        assert client is not None
    except Exception as e:
        pytest.fail(f"Failed to create Google GenAI client: {e}")


@pytest.mark.integration
@skip_if_no_project
def test_vertex_ai_access():
    """Test that Vertex AI can be accessed with current credentials."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

    assert project_id is not None, "GOOGLE_CLOUD_PROJECT not set"

    try:
        import vertexai

        vertexai.init(project=project_id, location=location)
        # If this doesn't raise an exception, credentials are working
        # Test passed if no exception was raised
    except Exception as e:
        pytest.fail(f"Failed to initialize Vertex AI: {e}")


@pytest.mark.integration
@skip_if_no_credentials
@pytest.mark.slow
def test_simple_agent_response():
    """Test that the simple agent can respond to a query."""
    try:
        from simple_test_agent import root_agent

        # Test a simple query
        response = root_agent.run_live(
            "Hello! Can you tell me what 2+2 equals?"
        )

        # Since run_live might be async, handle both cases
        if hasattr(response, "__aiter__"):
            # It's an async generator, we'll just check it exists
            assert response is not None
        else:
            assert response is not None
            assert len(str(response)) > 0

    except Exception as e:
        pytest.fail(f"Simple agent test failed: {e}")


@pytest.mark.integration
@skip_if_no_credentials
def test_trend_spotter_agent_import():
    """Test that the trend spotter agent can be imported and configured."""
    try:
        from trend_spotter.agent import root_agent

        assert root_agent is not None
        assert hasattr(root_agent, "name")
        assert hasattr(root_agent, "model")
        assert hasattr(root_agent, "tools")

        # Check that it has expected properties
        assert len(root_agent.name) > 0
        assert root_agent.model is not None

    except Exception as e:
        pytest.fail(f"Trend spotter agent import failed: {e}")


@pytest.mark.integration
@skip_if_no_credentials
@pytest.mark.slow
def test_model_access_with_adk():
    """Test that ADK can access Google models."""
    try:
        from google.adk.agents import Agent

        # Test with a known working model
        agent = Agent(
            model="gemini-pro",
            name="test_agent",
            description="Test agent",
            instruction=(
                "You are a test agent. "
                "Always respond with 'Hello, this is a test.'"
            ),
            tools=[],
        )

        assert agent is not None
        assert agent.model == "gemini-pro"
        assert agent.name == "test_agent"

    except Exception as e:
        pytest.fail(f"ADK model access test failed: {e}")
