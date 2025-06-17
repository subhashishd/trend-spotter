#!/usr/bin/env python3
"""
Test script for the email agent functionality.
Run this to verify that email configuration is working correctly.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def test_email_configuration():
    """
    Test if email environment variables are configured.
    """
    print("🔍 Checking email configuration...")

    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_APP_PASSWORD")

    assert sender_email is not None, "SENDER_EMAIL environment variable not set"
    assert (
        sender_password is not None
    ), "SENDER_APP_PASSWORD environment variable not set"

    print(f"✅ SENDER_EMAIL: {sender_email}")
    print(f"✅ SENDER_APP_PASSWORD: {'*' * len(sender_password)} (hidden)")


def test_email_agent():
    """
    Test the email agent with a sample report.
    """
    print("\n📧 Testing email agent...")

    # Sample trend report for testing
    sample_report = """
# AI Agent Trends Report - Test (December 13-19, 2024)

**🔥 Top 5 Trends for Agent Developers**

1. **Multi-Agent Systems**: Growing focus on orchestrating multiple AI agents
for complex tasks. **(Source: https://example.com/multi-agent)**
   * **Developer Impact**: Enables building more sophisticated AI applications
with specialized agents.
   * **Prioritization Rationale**: High discussion volume on Reddit and multiple
tech articles.

2. **Agent Framework Standardization**: Emerging standards for agent
communication protocols. **(Source: https://example.com/standards)**
   * **Developer Impact**: Reduces integration complexity between different
agent frameworks.
   * **Prioritization Rationale**: Critical for ecosystem development.

**🚀 Top 5 Releases for Agent Developers**

1. **AgentSDK v2.0**: New release with enhanced multi-modal capabilities.
**(Source: https://example.com/agentsdk)**
   * **Developer Impact**: Simplifies building agents that work with text,
images, and audio.
   * **Prioritization Rationale**: Major version release with significant new
features.

**🤔 Top 5 Questions from Agent Developers**

1. **"How to handle agent memory efficiently?"**: Developers seeking best
practices for persistent memory. **(Source: https://example.com/memory)**
   * **Developer Impact**: Critical for building stateful, context-aware agents.
   * **Prioritization Rationale**: Frequently asked question across multiple
communities.
    """

    # Test the email function directly to avoid async complexity
    from trend_spotter.sub_agents.email_agent import send_email_report

    response = send_email_report(
        subject="AI Agent Trends Report - Test (December 13-19, 2024)",
        report_content=sample_report,
        report_date_range="December 13-19, 2024",
    )

    print(f"📤 Email function response: {response}")
    assert "✅" in response


def test_email_recipients():
    """
    Test email recipients configuration.
    """
    print("\n📋 Testing email recipients configuration...")

    recipients_env = os.getenv("EMAIL_RECIPIENTS", "")
    if recipients_env:
        recipients = [
            email.strip() for email in recipients_env.split(",") if email.strip()
        ]
        print(f"✅ EMAIL_RECIPIENTS configured: {', '.join(recipients)}")
    else:
        print("⚠️ EMAIL_RECIPIENTS not set, will use default: <your email address>")
    # Test always passes - configuration is optional


def main():
    """
    Main test function.
    """
    print("🧪 Email Agent Test Suite")
    print("=" * 40)

    # Test configuration
    if not test_email_configuration():
        print("\n❌ Email configuration test failed!")
        print("\n📋 Setup Instructions:")
        print("1. Set SENDER_EMAIL environment variable")
        print("2. Set SENDER_APP_PASSWORD environment variable")
        print("3. Optionally set EMAIL_RECIPIENTS for multiple recipients")
        print("4. See email_config.md for detailed setup instructions")
        return

    # Test recipients configuration
    test_email_recipients()

    # Test email sending
    if test_email_agent():
        print("\n✅ All email tests passed!")
        recipients_env = os.getenv("EMAIL_RECIPIENTS", "<your email address>")
        recipients = [
            email.strip() for email in recipients_env.split(",") if email.strip()
        ]
        print(
            f"📧 Check the following email(s) for the test report: {', '.join(recipients)}"
        )
    else:
        print("\n❌ Email sending test failed!")
        print("🔧 Check your email configuration and network connection.")


if __name__ == "__main__":
    main()
