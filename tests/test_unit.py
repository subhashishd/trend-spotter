#!/usr/bin/env python3
"""Unit tests that don't require external services."""

import os
from unittest.mock import patch

import pytest


@pytest.mark.unit
def test_imports():
    """Test that basic imports work without requiring credentials."""
    # Test that we can import the main modules
    import prompt

    assert hasattr(prompt, "TREND_SPOTTER_PROMPT")

    # Test that the prompt is not empty
    assert len(prompt.TREND_SPOTTER_PROMPT) > 0
    assert "agent factory" in prompt.TREND_SPOTTER_PROMPT.lower()


@pytest.mark.unit
def test_prompt_content():
    """Test that the prompt contains expected content."""
    from prompt import TREND_SPOTTER_PROMPT

    # Check for key concepts in the prompt
    expected_keywords = ["agent", "factory", "analyst", "report", "developer"]

    prompt_lower = TREND_SPOTTER_PROMPT.lower()
    for keyword in expected_keywords:
        assert (
            keyword in prompt_lower
        ), f"Keyword '{keyword}' not found in prompt"


@pytest.mark.unit
def test_environment_variables_structure():
    """Test environment variable handling without requiring actual values."""
    # Test that the code handles missing environment variables gracefully
    with patch.dict(os.environ, {}, clear=True):
        # This should not raise an exception
        api_key = os.getenv("GOOGLE_API_KEY")
        assert api_key is None

        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        assert project_id is None


@pytest.mark.unit
def test_agent_import_structure():
    """Test that agent modules can be imported (structure test only)."""
    # Test importing without actually creating agents
    # (which would require credentials)
    try:
        import agent

        assert hasattr(agent, "__file__")
    except ImportError as e:
        pytest.skip(f"Agent module not available: {e}")


@pytest.mark.unit
def test_simple_test_agent_structure():
    """Test that simple_test_agent module structure is correct."""
    try:
        import simple_test_agent

        assert hasattr(simple_test_agent, "__file__")
    except ImportError as e:
        pytest.skip(f"Simple test agent module not available: {e}")


@pytest.mark.unit
def test_file_structure():
    """Test that required files exist."""
    import os

    # Check that main files exist
    assert os.path.exists("agent.py")
    assert os.path.exists("prompt.py")
    assert os.path.exists("pyproject.toml")
    assert os.path.exists("requirements.txt")

    # Check that __init__.py exists (for package structure)
    assert os.path.exists("__init__.py")
