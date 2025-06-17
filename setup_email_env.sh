#!/bin/bash

# Setup script for Email Agent Environment Variables
# This script helps set up the required environment variables for the email agent

echo "🔧 Email Agent Environment Setup"
echo "================================="
echo

# Check if .env file exists
if [ -f ".env" ]; then
    echo "✅ Found existing .env file"
    echo "📋 Current email configuration:"
    grep -E "^(SENDER_EMAIL|SENDER_APP_PASSWORD|EMAIL_RECIPIENTS|SMTP_SERVER|SMTP_PORT)=" .env 2>/dev/null | sed 's/SENDER_APP_PASSWORD=.*/SENDER_APP_PASSWORD=***hidden***/' || echo "⚠️  No email configuration found in .env"
else
    echo "⚠️  No .env file found"
    echo "📝 You can create one manually or let this script help you"
fi

echo
echo "📧 Email Configuration Instructions:"
echo "1. Gmail Setup:"
echo "   - Enable 2FA on your Google Account"
echo "   - Generate an App Password: Google Account > Security > App passwords"
echo "   - Use 'Trend Spotter' as the app name"
echo "   - Copy the 16-character password"
echo
echo "2. Environment Variables:"
echo "   SENDER_EMAIL: Your Gmail address (e.g., youremail@gmail.com)"
echo "   SENDER_APP_PASSWORD: The 16-character app password from step 1"
echo "   EMAIL_RECIPIENTS: Comma-separated recipient list (e.g., user1@example.com,user2@example.com)"
echo
echo "3. Example Configuration (for your .env file):"
echo "   SENDER_EMAIL=<your email address>"
echo "   SENDER_APP_PASSWORD=<your app password>"
echo "   EMAIL_RECIPIENTS=<recipient email addresses>"
echo

# Test current configuration
echo "🧪 Testing current configuration..."
echo

if [ -f ".env" ]; then
    source .env
fi

if [ -z "$SENDER_EMAIL" ]; then
    echo "❌ SENDER_EMAIL not set"
else
    echo "✅ SENDER_EMAIL: $SENDER_EMAIL"
fi

if [ -z "$SENDER_APP_PASSWORD" ]; then
    echo "❌ SENDER_APP_PASSWORD not set"
else
    echo "✅ SENDER_APP_PASSWORD: $(echo "$SENDER_APP_PASSWORD" | sed 's/./*/g') (hidden)"
fi

if [ -z "$EMAIL_RECIPIENTS" ]; then
    echo "⚠️  EMAIL_RECIPIENTS not set, will use default: <your email address>"
else
    echo "✅ EMAIL_RECIPIENTS: $EMAIL_RECIPIENTS"
fi

echo
echo "🚀 Next Steps:"
echo "1. If configuration looks correct, test the email agent:"
echo "   python tests/email/test_email_agent.py"
echo
echo "2. If you need to modify the configuration:"
echo "   - Edit the .env file directly"
echo "   - Or use export commands in your terminal"
echo
echo "3. For multiple recipients, format as:"
echo "   EMAIL_RECIPIENTS=user1@example.com,user2@example.com,user3@example.com"
echo
echo "4. For GitHub deployment, add these secrets to your repository:"
echo "   - SENDER_EMAIL"
echo "   - SENDER_APP_PASSWORD"
echo "   - EMAIL_RECIPIENTS"
echo
echo "📚 For detailed setup instructions, see: documentation/email_config.md"
echo "🔐 For GitHub secrets setup, see: documentation/GITHUB_SECRETS_SETUP.md"

