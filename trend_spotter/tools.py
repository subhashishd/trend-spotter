import os
import praw


# The function now accepts a LIST of subreddit names
def search_hot_reddit_posts(
    subreddit_names: list[str], limit_per_subreddit: int = 5
) -> str:
    """
    Searches a list of subreddits for their current hot posts and returns their titles and URLs.

    Args:
        subreddit_names: A list of subreddit names to search (e.g., ["LocalLLaMA", "MachineLearning"]).
        limit_per_subreddit: The number of top posts to retrieve from each subreddit.

    Returns:
        A dictionary containing the status and a list of formatted post strings.
    """
    try:
        print(
            f"\n🔎 Searching Reddit for hot posts in: {', '.join(subreddit_names)}..."
        )

        reddit = praw.Reddit(
            client_id=os.environ["REDDIT_CLIENT_ID"],
            client_secret=os.environ["REDDIT_CLIENT_SECRET"],
            user_agent=os.environ["REDDIT_USER_AGENT"],
            read_only=True,
        )

        all_posts = []
        # Loop through each subreddit name provided in the list
        for sub_name in subreddit_names:
            print(f"  - Fetching from r/{sub_name}...")
            subreddit = reddit.subreddit(sub_name)
            for post in subreddit.hot(limit=limit_per_subreddit):
                # We can add a simple filter here if we want, e.g., for score
                if post.score > 5:
                    all_posts.append(f"Title: {post.title}\nLink: {post.url}")

        if not all_posts:
            return "No hot posts found meeting the criteria in the specified subreddits."

        print(
            f"✅ Reddit search complete. Found {len(all_posts)} qualifying posts."
        )
        return "\n---\n".join(all_posts)

    except Exception as e:
        return f"Error searching Reddit: {e}"
