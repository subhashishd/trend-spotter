# trend_spotter/sub_agents/reddit_agent.py
from google.adk.agents import Agent
from trend_spotter.tools import search_hot_reddit_posts

MODEL = "gemini-2.5-pro-preview-05-06"

reddit_agent = Agent(
    name="reddit_agent",
    model=MODEL,
    description="An expert at finding hot posts on specific Reddit subreddits using its tool.",
    tools=[search_hot_reddit_posts],
)
