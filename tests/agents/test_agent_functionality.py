#!/usr/bin/env python3
"""Test script to verify the agent works end-to-end with Vertex AI."""


from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_simple_agent_response():
    """Test if the simple agent can respond to a basic query."""
    from simple_test_agent import root_agent

    print("✅ Simple agent imported successfully")

    # Test a simple query
    response = root_agent.run_live("Hello! Can you tell me what 2+2 equals?")
    print(f"✅ Agent response: {response}")
    assert response is not None


def test_trend_spotter_agent_import():
    """Test if the trend spotter agent can be imported."""
    from trend_spotter.agent import root_agent

    print(f"✅ Trend spotter agent imported successfully: {root_agent.name}")
    print(f"✅ Model: {root_agent.model}")
    print(f"✅ Tools available: {len(root_agent.tools)} tool(s)")
    assert root_agent is not None
    assert len(root_agent.tools) == 3


if __name__ == "__main__":
    print("Testing Agent Functionality with Vertex AI...")
    print("=" * 50)

    success = True

    print("\n1. Testing simple agent response...")
    if not test_simple_agent_response():
        success = False

    print("\n2. Testing trend spotter agent import...")
    if not test_trend_spotter_agent_import():
        success = False

    print("\n" + "=" * 50)
    if success:
        print("\n🎉 All agent functionality tests passed!")
        print("Your Vertex AI integration is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
