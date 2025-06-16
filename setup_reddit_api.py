#!/usr/bin/env python3
"""
Reddit API Setup Helper

This script helps you configure Reddit API credentials for the trend spotter agent.
"""

import os
import webbrowser
from pathlib import Path


def setup_reddit_credentials():
    """Interactive setup for Reddit API credentials."""
    print("🚀 Reddit API Setup for Trend Spotter")
    print("=" * 50)
    
    print("\n📝 Step 1: Create Reddit Application")
    print("We'll open Reddit's app creation page for you...")
    
    # Open Reddit apps page
    reddit_apps_url = "https://www.reddit.com/prefs/apps"
    print(f"Opening: {reddit_apps_url}")
    webbrowser.open(reddit_apps_url)
    
    print("\n📋 Instructions:")
    print("1. Click 'Create App' or 'Create Another App'")
    print("2. Fill out the form:")
    print("   - Name: trend-spotter")
    print("   - App type: script")
    print("   - Description: AI agent for trend spotting on The Agent Factory podcast")
    print("   - About URL: (leave blank)")
    print("   - Redirect URI: http://localhost:8080")
    print("3. Click 'Create app'")
    
    input("\nPress Enter after you've created the Reddit app...")
    
    print("\n🔑 Step 2: Get Your Credentials")
    print("Now we need to collect your Reddit app credentials.")
    
    # Collect credentials
    client_id = input("\nEnter your Reddit Client ID (shown under the app name): ").strip()
    client_secret = input("Enter your Reddit Client Secret: ").strip()
    reddit_username = input("Enter your Reddit username (for user agent): ").strip()
    
    if not client_id or not client_secret or not reddit_username:
        print("❌ Error: All fields are required!")
        return False
    
    user_agent = f"trend-spotter:v1.0 (by /u/{reddit_username})"
    
    print("\n📋 Step 3: Configure Environment")
    
    # Update .env file
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file, 'r') as f:
            env_content = f.read()
        
        # Replace or add Reddit credentials
        lines = env_content.split('\n')
        new_lines = []
        reddit_section_found = False
        
        for line in lines:
            if line.startswith('# Reddit API Configuration'):
                reddit_section_found = True
                new_lines.extend([
                    '# Reddit API Configuration (Required for Reddit Agent)',
                    '# Get these from https://www.reddit.com/prefs/apps',
                    f'REDDIT_CLIENT_ID={client_id}',
                    f'REDDIT_CLIENT_SECRET={client_secret}',
                    f'REDDIT_USER_AGENT={user_agent}',
                    ''
                ])
                # Skip the old commented lines
                continue
            elif line.startswith('# REDDIT_') or line.startswith('REDDIT_'):
                # Skip old Reddit config lines
                continue
            else:
                new_lines.append(line)
        
        if not reddit_section_found:
            # Add Reddit section at the end
            new_lines.extend([
                '',
                '# Reddit API Configuration (Required for Reddit Agent)',
                '# Get these from https://www.reddit.com/prefs/apps',
                f'REDDIT_CLIENT_ID={client_id}',
                f'REDDIT_CLIENT_SECRET={client_secret}',
                f'REDDIT_USER_AGENT={user_agent}',
                ''
            ])
        
        with open(env_file, 'w') as f:
            f.write('\n'.join(new_lines))
        
        print(f"   ✅ Updated {env_file}")
    else:
        print("   ⚠️  .env file not found, creating new one...")
        with open(env_file, 'w') as f:
            f.write(f"""# Reddit API Configuration (Required for Reddit Agent)
# Get these from https://www.reddit.com/prefs/apps
REDDIT_CLIENT_ID={client_id}
REDDIT_CLIENT_SECRET={client_secret}
REDDIT_USER_AGENT={user_agent}
""")
        print(f"   ✅ Created {env_file}")
    
    print("\n🎉 Step 4: Test Configuration")
    print("Let's test your Reddit API credentials...")
    
    # Test the credentials
    try:
        import praw
        
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            read_only=True,
        )
        
        # Try to fetch a single post from a popular subreddit
        test_subreddit = reddit.subreddit('Python')
        test_post = next(test_subreddit.hot(limit=1))
        
        print(f"   ✅ Success! Retrieved post: '{test_post.title[:50]}...'")
        
    except Exception as e:
        print(f"   ❌ Error testing credentials: {e}")
        print("   Please verify your credentials and try again.")
        return False
    
    print("\n📝 Step 5: GitHub Secrets (For Production)")
    print("For production deployment, you'll also need to add these to GitHub secrets:")
    print("")
    print("Go to: https://github.com/subhashishd/trend-spotter/settings/secrets/actions")
    print("")
    print("Add these secrets:")
    print(f"   REDDIT_CLIENT_ID = {client_id}")
    print(f"   REDDIT_CLIENT_SECRET = {client_secret}")
    print(f"   REDDIT_USER_AGENT = {user_agent}")
    
    print("\n" + "=" * 50)
    print("🎉 Reddit API setup complete!")
    print("\nNext steps:")
    print("1. Test locally: adk web --port 8080")
    print("2. Add GitHub secrets for production deployment")
    print("3. Deploy: git push origin main")
    
    return True


def main():
    """Main setup function."""
    try:
        success = setup_reddit_credentials()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user.")
        return 1
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main())

