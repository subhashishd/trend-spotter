#!/usr/bin/env python3
"""
Direct test of the trend spotter agent to verify it works with Vertex AI.
"""

import asyncio
import sys

# Import third-party modules first
from google.adk import Runner

# Add current directory to path and import local modules
sys.path.insert(0, ".")
from agent import root_agent  # noqa: E402


async def test_agent():
    """Test the agent with a simple query."""
    print("Testing Trend Spotter Agent...")
    print(f"Agent: {root_agent.name}")
    print(f"Description: {root_agent.description}")

    # Create runner
    runner = Runner(agent=root_agent)

    print("\nSending query: 'What are the latest AI agent trends?'")
    print("=" * 60)

    try:
        # Use the runner to run the agent
        response = await runner.run_async(
            "What are the latest AI agent trends?"
        )
        print(response)
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback

        traceback.print_exc()
        return False

    print("\n" + "=" * 60)
    print("Agent test completed successfully!")
    return True


if __name__ == "__main__":
    asyncio.run(test_agent())
