# Simple test agent for Vertex AI without tools
from google.adk.agents import Agent

# Use gemini-pro model that is available in Vertex AI
MODEL = "gemini-pro"

# Create a simple agent without tools for testing
simple_test_agent = Agent(
    model=MODEL,
    name="simple_test_agent",
    description="A simple test agent for Vertex AI.",
    instruction=(
        "You are a helpful AI assistant. Respond to any question in a "
        "friendly and informative way."
    ),
    tools=[],  # No tools for now
)

# Export as root_agent for testing
root_agent = simple_test_agent
