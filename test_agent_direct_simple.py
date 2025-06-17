#!/usr/bin/env python3
"""Direct test of the agent without web interface."""

import asyncio
import sys
from dotenv import load_dotenv
from google.adk.runners import InvocationContext
from trend_spotter.agent import root_agent

# Add the project root to the path
sys.path.append(".")

# Load environment variables
load_dotenv()


async def test_agent_direct():
    """Test the agent directly without web interface."""
    print("🤖 Testing TrendSpotter agent directly...")

    try:
        # Create invocation context
        ctx = InvocationContext(
            agent=root_agent,
            user_id="test_user",
            request="Find the latest AI agent trends and email them to me",
        )

        print("📡 Starting agent execution...")

        # Run the agent
        async for event in root_agent.run_async(ctx):
            if hasattr(event, "content") and event.content:
                print(f"🔄 Agent: {event.content}")
            elif hasattr(event, "text") and event.text:
                print(f"🔄 Agent: {event.text}")

        print("✅ Agent execution completed successfully!")

    except Exception as e:
        print(f"❌ Agent execution failed: {str(e)}")
        import traceback

        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    print("Starting direct agent test...")
    success = asyncio.run(test_agent_direct())
    if success:
        print("\n🎉 Direct agent test completed successfully!")
    else:
        print("\n❌ Direct agent test failed.")
        sys.exit(1)
