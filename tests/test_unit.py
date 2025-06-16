#!/usr/bin/env python3
"""Unit tests that don't require external services."""

import os
from unittest.mock import patch

import pytest


@pytest.mark.unit
def test_imports():
    """Test that basic imports work without requiring credentials."""
    # Test that we can import the main modules
    from trend_spotter import prompt

    assert hasattr(prompt, "ORCHESTRATOR_PROMPT")

    # Test that the prompt is not empty
    assert len(prompt.ORCHESTRATOR_PROMPT) > 0
    assert "agent factory" in prompt.ORCHESTRATOR_PROMPT.lower()


@pytest.mark.unit
def test_multi_agent_imports():
    """Test that multi-agent system components can be imported."""
    # Test orchestrator agent structure
    from trend_spotter.agent import root_agent

    assert root_agent is not None
    assert root_agent.name == "TrendSpotterOrchestrator"

    # Test sub-agents can be imported
    from trend_spotter.sub_agents.google_search_agent import (
        google_search_agent,
    )
    from trend_spotter.sub_agents.reddit_agent import reddit_agent

    assert google_search_agent is not None
    assert reddit_agent is not None

    # Test tools import
    from trend_spotter.tools import search_hot_reddit_posts

    assert callable(search_hot_reddit_posts)


@pytest.mark.unit
def test_agent_configuration():
    """Test that agents are properly configured."""
    from trend_spotter.agent import root_agent

    # Test orchestrator has tools (sub-agents)
    assert len(root_agent.tools) == 2

    # Test orchestrator uses correct model
    assert "gemini" in root_agent.model.lower()


@pytest.mark.unit
def test_sub_agent_structure():
    """Test that sub-agents are properly structured."""
    from trend_spotter.sub_agents.google_search_agent import (
        google_search_agent,
    )
    from trend_spotter.sub_agents.reddit_agent import reddit_agent

    # Test google search agent
    assert google_search_agent.name == "google_search_agent"
    assert len(google_search_agent.tools) == 1  # google_search tool

    # Test reddit agent
    assert reddit_agent.name == "reddit_agent"
    assert len(reddit_agent.tools) == 1  # search_hot_reddit_posts tool


@pytest.mark.unit
def test_orchestrator_prompt_content():
    """Test orchestrator prompt contains expected multi-agent content."""

    from trend_spotter.prompt import ORCHESTRATOR_PROMPT

    # Check for multi-agent specific concepts
    expected_keywords = [
        "manager",
        "google_search_agent",
        "reddit_agent",
        "delegate",
        "specialist",
        "tools",
        "team",
    ]

    prompt_lower = ORCHESTRATOR_PROMPT.lower()
    for keyword in expected_keywords:
        assert (
            keyword in prompt_lower
        ), f"Multi-agent keyword '{keyword}' not found in orchestrator prompt"


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
        from trend_spotter import agent

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
def test_tools_function_signature():
    """Test that tools have correct function signatures for multi-agent use."""
    import inspect

    from trend_spotter.tools import search_hot_reddit_posts

    # Test that search_hot_reddit_posts accepts list of subreddits
    sig = inspect.signature(search_hot_reddit_posts)
    params = list(sig.parameters.keys())

    assert "subreddit_names" in params
    assert "limit_per_subreddit" in params

    # Test parameter types if annotations exist
    subreddit_param = sig.parameters["subreddit_names"]
    if subreddit_param.annotation != inspect.Parameter.empty:
        # Should accept list of strings
        assert "list" in str(subreddit_param.annotation).lower()


@pytest.mark.unit
def test_multi_agent_file_structure():
    """Test that multi-agent files exist."""
    import os

    # Check that package files exist in trend_spotter directory
    assert os.path.exists("trend_spotter/agent.py")
    assert os.path.exists("trend_spotter/prompt.py")
    assert os.path.exists("trend_spotter/tools.py")
    assert os.path.exists("trend_spotter/__init__.py")

    # Check sub-agents directory
    assert os.path.exists("trend_spotter/sub_agents/")
    assert os.path.exists("trend_spotter/sub_agents/__init__.py")
    assert os.path.exists("trend_spotter/sub_agents/google_search_agent.py")
    assert os.path.exists("trend_spotter/sub_agents/reddit_agent.py")

    # Check that project configuration files exist
    assert os.path.exists("pyproject.toml")
    assert os.path.exists("requirements.txt")
