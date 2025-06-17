# TrendSpotter Documentation

This folder contains all the documentation for the TrendSpotter AI multi-agent system.

## 📋 Documentation Index

### Core Architecture
- **[multi_agent_system.md](multi_agent_system.md)** - Complete overview of the multi-agent architecture, workflow, and technical implementation

### Setup & Configuration
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deployment instructions and configuration
- **[GITHUB_SECRETS_SETUP.md](GITHUB_SECRETS_SETUP.md)** - Setting up GitHub secrets for CI/CD
- **[email_config.md](email_config.md)** - Email configuration setup guide
- **[EMAIL_SETUP_COMPLETE.md](EMAIL_SETUP_COMPLETE.md)** - Complete email setup documentation

### Authentication & OAuth2
- **[GOOGLE_OAUTH2_SETUP.md](GOOGLE_OAUTH2_SETUP.md)** - Google OAuth2 authentication setup
- **[README_OAUTH2.md](README_OAUTH2.md)** - OAuth2 implementation details and usage

### Implementation Details
- **[EMAIL_AGENT_IMPLEMENTATION_SUMMARY.md](EMAIL_AGENT_IMPLEMENTATION_SUMMARY.md)** - Detailed implementation of the email agent
- **[VERTEX_AI_STATUS.md](VERTEX_AI_STATUS.md)** - Vertex AI integration status and notes

### Operations & Deployment
- **[PRODUCTION_DEPLOYMENT_CHECKLIST.md](PRODUCTION_DEPLOYMENT_CHECKLIST.md)** - Pre-deployment checklist and production considerations
- **[WORKFLOWS_README.md](WORKFLOWS_README.md)** - GitHub Actions workflows documentation

## 🚀 Quick Start

1. **First time setup**: Start with [DEPLOYMENT.md](DEPLOYMENT.md)
2. **Email features**: Configure using [email_config.md](email_config.md)
3. **Authentication**: Set up OAuth2 with [GOOGLE_OAUTH2_SETUP.md](GOOGLE_OAUTH2_SETUP.md)
4. **Production deployment**: Follow [PRODUCTION_DEPLOYMENT_CHECKLIST.md](PRODUCTION_DEPLOYMENT_CHECKLIST.md)

## 🏗️ Architecture Overview

TrendSpotter uses a multi-agent system with:
- **Orchestrator Agent**: Coordinates the workflow
- **Google Search Agent**: Performs web research
- **Reddit Agent**: Gathers community insights
- **Email Agent**: Delivers formatted reports

For detailed architecture information, see [multi_agent_system.md](multi_agent_system.md).

## 📧 Email Features

The system includes comprehensive email functionality:
- Professional HTML email templates
- Multiple recipient support
- SMTP configuration (Gmail, etc.)
- Delivery status tracking

## 🔐 Security & Authentication

- Google OAuth2 integration for web access
- Environment variable configuration
- GitHub secrets for CI/CD security
- Production-ready deployment options

## 📝 Contributing

When adding new documentation:
1. Place new .md files in this `documentation/` folder
2. Update this README.md index
3. Follow the existing naming conventions
4. Include setup instructions and examples

---

For the main project README and getting started guide, see [../README.md](../README.md).

