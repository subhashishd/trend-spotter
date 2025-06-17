# Email Agent Configuration

The email agent uses MCP (Model Context Protocol) compatible email tools to deliver trend reports via email.

## Required Environment Variables

To enable email functionality, you need to set the following environment variables:

```bash
# Email sender configuration
export SENDER_EMAIL="your-email@gmail.com"
export SENDER_APP_PASSWORD="your-app-specific-password"

# Optional SMTP configuration (defaults to Gmail)
export SMTP_SERVER="smtp.gmail.com"  # Default
export SMTP_PORT="587"                 # Default
```

## Gmail Setup Instructions

### 1. Enable 2-Factor Authentication
- Go to your Google Account settings
- Navigate to Security
- Enable 2-Step Verification

### 2. Generate App Password
- In Google Account Security settings
- Select "App passwords"
- Choose "Mail" and "Other (custom name)"
- Enter "Trend Spotter Agent" as the name
- Copy the generated 16-character password
- Use this password as `SENDER_APP_PASSWORD`

### 3. Set Environment Variables

**Option A: Export in terminal (temporary)**
```bash
export SENDER_EMAIL="youremail@gmail.com"
export SENDER_APP_PASSWORD="abcd efgh ijkl mnop"
```

**Option B: Add to your shell profile (permanent)**
```bash
# Add to ~/.zshrc or ~/.bashrc
echo 'export SENDER_EMAIL="youremail@gmail.com"' >> ~/.zshrc
echo 'export SENDER_APP_PASSWORD="abcd efgh ijkl mnop"' >> ~/.zshrc
source ~/.zshrc
```

**Option C: Use a .env file (for development)**
Create a `.env` file in the project root:
```
SENDER_EMAIL=youremail@gmail.com
SENDER_APP_PASSWORD=abcd efgh ijkl mnop
```

## Recipients Configuration

### Single Recipient (Default)
```bash
export EMAIL_RECIPIENTS="tinks70@gmail.com"
```

### Multiple Recipients
```bash
export EMAIL_RECIPIENTS="user1@example.com,user2@example.com,user3@example.com"
```

### Default Configuration
- **Default recipient**: tinks70@gmail.com (if EMAIL_RECIPIENTS not set)
- **Email format**: HTML with professional styling
- **Subject format**: "AI Agent Trends Report - [Date Range]"
- **SMTP server**: Gmail (smtp.gmail.com:587)
- **Multiple recipient support**: Yes (comma-separated list)

## Security Notes

1. **Never commit credentials to version control**
2. **Use app-specific passwords, not your main Gmail password**
3. **The email agent will fail gracefully if credentials are missing**
4. **All email communication uses TLS encryption**

## Testing the Email Agent

To test email functionality:

```python
from trend_spotter.sub_agents.email_agent import email_agent

# Test with a simple message
response = email_agent.run(
    "Please send a test email with the subject 'Test Email' to tinks70@gmail.com with some sample content."
)

print(response)
```

## Troubleshooting

### Common Issues:

1. **"Email credentials not configured"**
   - Check that SENDER_EMAIL and SENDER_APP_PASSWORD are set
   - Run `echo $SENDER_EMAIL` to verify

2. **"Authentication failed"**
   - Verify the app password is correct
   - Ensure 2FA is enabled on your Google account
   - Try generating a new app password

3. **"Connection refused"**
   - Check your internet connection
   - Verify SMTP server and port settings
   - Some corporate networks block SMTP

4. **"Permission denied"**
   - Make sure "Less secure app access" is disabled (we use app passwords instead)
   - Check that your Google account has email sending permissions

## MCP Integration

This email agent follows MCP (Model Context Protocol) patterns:

- **Tool-based architecture**: Email functionality is exposed as a tool
- **Structured parameters**: Clear parameter definitions with types
- **Error handling**: Graceful failure with detailed error messages
- **Stateless operation**: Each email operation is independent
- **JSON response format**: Structured success/error responses

## Custom Email Templates

The email agent automatically converts markdown reports to HTML with:

- Professional styling with CSS
- Responsive design for mobile devices
- Proper email client compatibility
- Emoji support for visual appeal
- Clickable source links
- Header with report metadata
- Footer with generation timestamp

