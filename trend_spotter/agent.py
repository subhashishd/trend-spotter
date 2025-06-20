# trend_spotter/agent.py

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import __version__, prompt
from .sub_agents.email_agent import email_agent

# Import the sub-agent INSTANCES
from .sub_agents.google_search_agent import google_search_agent
from .sub_agents.reddit_agent import reddit_agent

MODEL = "gemini-2.5-flash-preview-05-20"
# This is our main "manager" agent, now an LlmAgent
root_agent = LlmAgent(
    model=MODEL,
    name="TrendSpotterOrchestrator",
    description=(f"The manager of a team of specialist AI agents (v{__version__})."),
    instruction=prompt.ORCHESTRATOR_PROMPT,
    # The Orchestrator's "tools" are its sub-agents, wrapped in AgentTool
    tools=[
        AgentTool(agent=google_search_agent),
        AgentTool(agent=reddit_agent),
        AgentTool(agent=email_agent),
    ],
)
