# trend_spotter/sub_agents/email_agent.py
from google.adk.agents import Agent
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import re
from datetime import datetime
from typing import Optional

MODEL = "gemini-2.5-flash-preview-05-20"


# MCP-style email tool implementation using ADK function pattern
def send_email_report(
    subject: str,
    report_content: str,
    report_date_range: str = "N/A",
    recipient_email: Optional[str] = None,
) -> str:
    """
    Send a formatted trend report via email to specified recipients.

    Args:
        subject: Email subject line
        report_content: The formatted trend report content to send
        report_date_range: Date range covered by the report (for email header)
        recipient_email: Optional specific recipient email (if not provided, uses EMAIL_RECIPIENTS env var)

    Returns:
        A JSON string with the status of the email sending operation
    """
    try:
        # Get recipients from environment variable or use provided recipient
        if recipient_email:
            recipients = [recipient_email.strip()]
        else:
            recipients_env = os.getenv("EMAIL_RECIPIENTS", "tinks70@gmail.com")
            recipients = [
                email.strip()
                for email in recipients_env.split(",")
                if email.strip()
            ]

        print(
            f"\n📧 Preparing to send email to {len(recipients)} recipient(s): {', '.join(recipients)}..."
        )

        # Get email configuration from environment variables
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv(
            "SENDER_APP_PASSWORD"
        )  # App-specific password for Gmail

        if not sender_email or not sender_password:
            error_msg = "Email credentials not configured. Please set SENDER_EMAIL and SENDER_APP_PASSWORD environment variables."
            print(f"❌ {error_msg}")
            return f"❌ Email failed: {error_msg}"

        # Create HTML email body
        html_body = _format_report_as_html(report_content, report_date_range)

        # Send email to all recipients
        sent_to = []
        failed_to = []

        print(f"📤 Connecting to SMTP server {smtp_server}:{smtp_port}...")
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Enable security
            server.login(sender_email, sender_password)

            for recipient in recipients:
                try:
                    # Create individual email message for each recipient
                    msg = MIMEMultipart()
                    msg["From"] = sender_email
                    msg["To"] = recipient
                    msg["Subject"] = subject
                    msg.attach(MIMEText(html_body, "html"))

                    text = msg.as_string()
                    server.sendmail(sender_email, recipient, text)
                    sent_to.append(recipient)
                    print(f"✅ Email sent to {recipient}")
                except Exception as e:
                    failed_to.append(f"{recipient} ({str(e)})")
                    print(f"❌ Failed to send to {recipient}: {str(e)}")

        # Generate summary message
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        if sent_to and not failed_to:
            success_msg = f"✅ Email successfully sent to {len(sent_to)} recipient(s): {', '.join(sent_to)} at {timestamp}"
        elif sent_to and failed_to:
            success_msg = f"⚠️ Email sent to {len(sent_to)} recipient(s): {', '.join(sent_to)}. Failed for {len(failed_to)}: {', '.join(failed_to)} at {timestamp}"
        else:
            success_msg = f"❌ Email failed for all {len(failed_to)} recipient(s): {', '.join(failed_to)} at {timestamp}"

        print(success_msg)
        return success_msg

    except Exception as e:
        error_msg = f"❌ Failed to send email to {recipient_email}: {str(e)}"
        print(error_msg)
        return error_msg


def _format_report_as_html(report_content: str, date_range: str) -> str:
    """
    Convert the markdown-style report to HTML for better email formatting.
    """
    # Convert basic markdown to HTML
    html_content = _convert_markdown_to_html(report_content)

    # Basic HTML template with styling
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>AI Agent Trends Report - {date_range}</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f9f9f9;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 10px;
                text-align: center;
                margin-bottom: 30px;
            }}
            .content {{
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .trend-item {{
                background: #f8f9fa;
                border-left: 4px solid #667eea;
                padding: 15px;
                margin-bottom: 15px;
                border-radius: 5px;
            }}
            .trend-title {{
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 5px;
            }}
            .source-link {{
                color: #667eea;
                text-decoration: none;
            }}
            .source-link:hover {{
                text-decoration: underline;
            }}
            .impact, .rationale {{
                margin: 8px 0;
                padding-left: 15px;
                color: #555;
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                padding: 20px;
                color: #777;
                font-size: 0.9em;
            }}
            h1, h2 {{
                color: #2c3e50;
            }}
            .emoji {{
                font-size: 1.2em;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🤖 AI Agent Trends Report</h1>
            <p><strong>Report Period:</strong> {date_range}</p>
            <p>Generated by The Agent Factory Intelligence System</p>
        </div>
        
        <div class="content">
            {html_content}
        </div>
        
        <div class="footer">
            <p>📧 This report was automatically generated and sent by your AI Agent Trend Spotter</p>
            <p>🕒 Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
        </div>
    </body>
    </html>
    """

    return html_template


def _convert_markdown_to_html(markdown_content: str) -> str:
    """
    Convert basic markdown formatting to HTML.
    """
    html_content = markdown_content

    # Basic conversion - just preserve the content with line breaks
    html_content = html_content.replace("\n", "<br>\n")

    # Convert headers
    html_content = html_content.replace(
        "**🔥 Top 5 Trends for Agent Developers**",
        '<h2 class="emoji">🔥 Top 5 Trends for Agent Developers</h2>',
    )
    html_content = html_content.replace(
        "**🚀 Top 5 Releases for Agent Developers**",
        '<h2 class="emoji">🚀 Top 5 Releases for Agent Developers</h2>',
    )
    html_content = html_content.replace(
        "**🤔 Top 5 Questions from Agent Developers**",
        '<h2 class="emoji">🤔 Top 5 Questions from Agent Developers</h2>',
    )

    # Bold formatting
    html_content = re.sub(
        r"\*\*(.*?)\*\*", r"<strong>\1</strong>", html_content
    )

    return html_content


# Email agent with specific instructions for handling report delivery
EMAIL_AGENT_PROMPT = """
**Role:**
- You are a specialist Email Delivery Agent.
- Your sole purpose is to receive a completed trend report and send it via email to the specified recipient.
- You have access to one tool: `send_email_report`.

**Context:**
- You will receive a completed trend report from the manager agent as a request.
- The request will contain the full report content that needs to be emailed.
- You must extract the relevant information and use your tool to send the email.
- Always use professional email formatting and include the date range in the subject.

**Task:**
1. Parse the request to extract the trend report content.
2. Look for the date range in the report (usually in the header like "Report Date Range: [dates]").
3. Create an appropriate email subject line that includes the date range.
4. Use the `send_email_report` tool with the correct parameters:
   - subject: "AI Agent Trends Report - [Date Range]"
   - report_content: The full report content
   - report_date_range: The extracted date range
   - recipient_email: "tinks70@gmail.com" (default)
5. Confirm successful delivery with a status message.

**Email Configuration:**
- Default recipient: tinks70@gmail.com (unless otherwise specified)
- Subject format: "AI Agent Trends Report - [Date Range]"
- Always include the full report content in the email body.

**Important:**
- When you receive a request with report content, immediately use the `send_email_report` tool.
- Do NOT try to format or modify the report content - send it as-is.
- Extract the date range from phrases like "Report Date Range: June 10, 2025 - June 17, 2025".

**Output:**
- Provide a clear confirmation of email delivery status.
- Include recipient, subject, and timestamp in your response.
"""

email_agent = Agent(
    name="email_agent",
    model=MODEL,
    description=(
        "A specialist agent for delivering trend reports via email using MCP-compatible tools."
    ),
    instruction=EMAIL_AGENT_PROMPT,
    tools=[send_email_report],
)
