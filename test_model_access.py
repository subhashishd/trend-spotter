#!/usr/bin/env python3
"""Test specific model access in Vertex AI."""


from dotenv import load_dotenv

load_dotenv()


def test_model_with_adk():
    """Test model access using the ADK Agent class."""
    try:
        from google.adk.agents import Agent

        # Test different models with the ADK Agent
        # Put working models first
        models_to_test = [
            "gemini-pro",
            "gemini-1.5-pro-002",
            "gemini-1.5-flash-002",
            "gemini-2.0-flash-001",
            "gemini-1.0-pro",  # This one doesn't work but kept for reference
            "text-bison",
        ]

        for model_name in models_to_test:
            try:
                print(f"Testing model: {model_name}")
                agent = Agent(
                    model=model_name,
                    name="test_agent",
                    description="Test agent",
                    instruction=(
                        "You are a test agent. "
                        "Always respond with 'Hello, this is a test.'"
                    ),
                    tools=[],
                )
                print(f"✅ {model_name} - Agent created successfully")
                return model_name, agent
            except Exception as e:
                print(f"❌ {model_name} - Error: {str(e)[:100]}...")

        return None, None

    except Exception as e:
        print(f"❌ Error importing ADK: {e}")
        return None, None


if __name__ == "__main__":
    print("Testing Model Access with ADK...")
    print("=" * 40)

    working_model, agent = test_model_with_adk()

    if working_model:
        print(f"\n🎉 SUCCESS! Working model found: {working_model}")
        print("Your agents should work with the web interface now.")
    else:
        print("\n❌ No working models found.")
        print("This indicates a Vertex AI access or configuration issue.")
