#!/usr/bin/env python3
"""Final comprehensive test for Vertex AI integration."""

import asyncio

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


async def test_agent_with_vertex_ai():
    """Test that the agent can actually communicate with Vertex AI."""
    try:
        from simple_test_agent import root_agent

        print("✅ Agent imported successfully")

        # Use the async generator properly
        print("🔄 Testing agent communication with Vertex AI...")

        response = await root_agent.run_async("What is 2+2? Keep your answer brief.")
        print(f"✅ Vertex AI Response: {response}")

        return True
    except Exception as e:
        print(f"❌ Error testing agent with Vertex AI: {e}")
        import traceback

        traceback.print_exc()
        return False


def run_test():
    """Run the async test."""
    return asyncio.run(test_agent_with_vertex_ai())


if __name__ == "__main__":
    print("Final Vertex AI Integration Test")
    print("=" * 40)

    if run_test():
        print("\n🎉 SUCCESS! Your Vertex AI integration is working perfectly!")
        print("The trend_spotter application is ready to use.")
    else:
        print("\n❌ FAILED! There are still issues with the Vertex AI integration.")
