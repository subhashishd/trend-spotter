# trend_spotter/agent.py

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

# Import the sub-agent INSTANCES
from .sub_agents.google_search_agent import google_search_agent
from .sub_agents.reddit_agent import reddit_agent
from . import prompt

MODEL = "gemini-2.5-pro-preview-05–06"
# This is our main "manager" agent, now an LlmAgent
root_agent = LlmAgent(
    model=MODEL,
    name="TrendSpotterOrchestrator",
    description="The manager of a team of specialist AI agents.",
    instruction=prompt.ORCHESTRATOR_PROMPT,
    # The Orchestrator's "tools" are its sub-agents, wrapped in AgentTool
    tools=[
        AgentTool(agent=google_search_agent),
        AgentTool(agent=reddit_agent),
    ],
)
