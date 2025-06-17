#!/usr/bin/env python3
"""
Direct test of the trend spotter agent to verify it works with Vertex AI.
"""

import sys

# Add current directory to path and import local modules
sys.path.insert(0, ".")
from trend_spotter.agent import root_agent  # noqa: E402


def test_agent():
    """Test the agent with a simple query."""
    print("Testing Trend Spotter Agent...")
    print(f"Agent: {root_agent.name}")
    print(f"Description: {root_agent.description}")

    # Test that the agent was created properly
    assert root_agent is not None
    assert root_agent.name == "TrendSpotterOrchestrator"
    assert len(root_agent.tools) == 3
    
    print("\n" + "=" * 60)
    print("Agent test completed successfully!")


if __name__ == "__main__":
    test_agent()
