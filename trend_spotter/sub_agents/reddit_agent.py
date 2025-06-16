# trend_spotter/sub_agents/reddit_agent.py
from google.adk.agents import Agent

from trend_spotter.tools import search_hot_reddit_posts

MODEL = "gemini-2.5-flash-preview-05-20"

reddit_agent = Agent(
    name="reddit_agent",
    model=MODEL,
    description=(
        "An expert at finding hot posts on specific Reddit subreddits "
        "using its tool."
    ),
    tools=[search_hot_reddit_posts],
)
