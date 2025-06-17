# TrendSpotter Multi-Agent System v0.1.2

An intelligent **multi-agent AI system** built with Google's Agent Development Kit (ADK) that automatically discovers, analyzes, and reports on the latest AI agent trends and developments.

> 🎆 **New in v0.1.2**: Added Email Agent with MCP-compatible email delivery! Reports are now automatically formatted and sent via email.
> 
> 🎆 **Multi-Agent System**: TrendSpotter has evolved from a single agent to a sophisticated multi-agent system! See [MULTI_AGENT_SYSTEM.md](./MULTI_AGENT_SYSTEM.md) for detailed architecture documentation.

## Summary

The Trend Spotter Agent is designed to keep developers and researchers up-to-date with the rapidly evolving AI agent landscape. It leverages Google Search to find recent developments, analyzes multiple sources, and generates structured reports covering:

- **Latest Trends**: Major developments in AI agent technology from the past 7 days
- **Recent Releases**: New frameworks, tools, platforms, and research papers
- **Developer Insights**: Thought-provoking questions and analysis for the AI community

The agent provides comprehensive reports with evidence-backed analysis, helping users stay informed about cutting-edge developments in AI agent technology.

## Technical Prerequisites

### Required Software
- **Python 3.9+**: The project requires Python 3.9 or later
- **pip**: Python package installer
- **Git**: For cloning and version control

### Google Cloud Setup
- **Google Cloud Project**: Active GCP project with billing enabled
- **Vertex AI API**: Must be enabled in your project
- **Authentication**: Application Default Credentials (ADC) configured
- **Regional Access**: Ensure your project has access to Gemini models in your chosen region

### API Access
- **Google Search**: Integrated through ADK's google_search tool
- **Vertex AI Models**: Access to Gemini models (gemini-1.5-pro or similar)
- **Email Service**: SMTP access for automated report delivery (optional)

## Project Structure

```
trend_spotter/
├── README.md                      # This file - project documentation
├── pyproject.toml                 # Project configuration, dependencies, and tool settings
├── requirements.txt               # Python dependencies
├── .env                          # Environment variables (create from template)
├── start_web.sh                  # Shell script to start the web interface
├── deploy.sh                     # Deployment script for Google Cloud Run
├── DEPLOYMENT.md                 # Comprehensive deployment guide
├── GITHUB_SECRETS_SETUP.md       # GitHub Actions secrets setup guide
├── VERTEX_AI_STATUS.md           # Vertex AI configuration status
├── trend_spotter/               # Main package directory
│   ├── __init__.py             # Package initialization for ADK discovery
│   ├── agent.py                # Main agent definition and configuration
│   └── prompt.py               # Detailed prompts and instructions for the agent
├── tests/                       # Test suite directory
│   ├── __init__.py             # Test package initialization
│   ├── test_unit.py            # Unit tests
│   └── test_integration.py     # Integration tests with external services
├── .github/                     # GitHub Actions workflows and configuration
│   ├── dependabot.yml          # Automated dependency updates
│   └── workflows/               # CI/CD workflows
│       ├── ci.yml              # Comprehensive CI/CD pipeline
│       ├── code-quality.yml    # Code quality checks (linting, formatting)
│       ├── deploy-adk.yml      # ADK deployment to Google Cloud Run
│       └── README.md           # Workflow documentation
├── myenv/                       # Virtual environment (created during setup)
├── test_*.py                    # Various standalone test scripts
└── trend_spotter.egg-info/      # Package build artifacts
```

## Main Files and Functionality

### Core Agent Files

#### `agent.py`
- **Purpose**: Main agent definition using Google ADK framework
- **Key Components**:
  - Agent configuration with Vertex AI Gemini model
  - Integration with Google Search tool
  - Connects agent logic to the detailed prompt system
- **Model**: Currently configured for `gemini-1.5-pro`

#### `prompt.py`
- **Purpose**: Contains the comprehensive multi-step prompt engineering
- **Key Features**:
  - Structured search strategy for recent AI agent trends
  - Guidelines for analyzing and synthesizing information
  - Template for generating organized reports
  - Instructions for creating developer-focused insights

#### `__init__.py`
- **Purpose**: Makes the directory a Python package and exposes the agent
- **Functionality**: Allows ADK to discover and load the `root_agent`

### Configuration Files

#### `pyproject.toml`
- **Purpose**: Project metadata and ADK agent registration
- **Key Settings**:
  - Project name and version
  - ADK agent discovery configuration
  - Maps `trend_spotter` to the agent module

#### `.env`
- **Purpose**: Environment variables for Google Cloud configuration
- **Required Variables**:
  - `GOOGLE_CLOUD_PROJECT`: Your GCP project ID
  - `GOOGLE_CLOUD_LOCATION`: Your preferred region (e.g., us-central1)
  - `GOOGLE_GENAI_USE_VERTEXAI`: Set to "true" for Vertex AI

#### `requirements.txt`
- **Purpose**: Lists all Python dependencies
- **Key Dependencies**:
  - Google ADK (`google-adk`)
  - Vertex AI SDK (`google-cloud-aiplatform`)
  - Additional supporting libraries

### Utility Files

#### `start_web.sh`
- **Purpose**: Convenience script to start the ADK web interface
- **Features**: 
  - Activates virtual environment
  - Validates Vertex AI configuration
  - Starts web server on localhost:8080

## Configuration and Setup

### 1. Clone and Setup

```bash
# Clone the repository
cd /path/to/your/workspace
git clone <repository-url>
cd trend_spotter

# Create and activate virtual environment
python3 -m venv myenv
source myenv/bin/activate  # On macOS/Linux
# OR
myenv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Google Cloud Configuration

#### Enable Required APIs
```bash
# Enable Vertex AI API
gcloud services enable aiplatform.googleapis.com

# Verify your project
gcloud config get-value project
```

#### Set up Authentication
```bash
# Authenticate with Google Cloud
gcloud auth application-default login

# Verify authentication
gcloud auth application-default print-access-token
```

### 3. Environment Configuration

Create a `.env` file in the project root:

```bash
# Copy the template and edit
cp .env.template .env  # If template exists
# OR create manually:
echo "GOOGLE_CLOUD_PROJECT=your-project-id" > .env
echo "GOOGLE_CLOUD_LOCATION=us-central1" >> .env
echo "GOOGLE_GENAI_USE_VERTEXAI=true" >> .env
```

Replace `your-project-id` with your actual Google Cloud project ID.

### 4. Install the Agent Package

```bash
# Install in development mode
pip install -e .
```

### 5. Verify Configuration

```bash
# Test Vertex AI connectivity
python test_vertex_ai.py

# Test agent loading
python -c "import trend_spotter; print('Agent loaded successfully!')"
```

## Running the Agent

### Option 1: Web Interface (Recommended)

```bash
# Start the web interface
./start_web.sh

# OR manually:
source myenv/bin/activate
adk web . --port 8080
```

Then open your browser to: http://localhost:8080

### Option 2: Command Line Interface

```bash
# Activate environment
source myenv/bin/activate

# Run interactively
adk run .

# Then type your queries, for example:
# "What are the latest AI agent trends?"
```

### Option 3: Direct Python Integration

```python
import asyncio
from trend_spotter import root_agent
from google.adk import Runner

async def run_query():
    runner = Runner(agent=root_agent)
    response = await runner.run_async("What are the latest AI agent trends?")
    print(response)

asyncio.run(run_query())
```

## Email Agent (MCP Integration)

TrendSpotter now includes an email delivery agent that automatically sends formatted reports to specified recipients using MCP (Model Context Protocol) compatible email tools.

### Email Configuration

To enable email functionality, set up the following environment variables:

```bash
# Required email configuration
export SENDER_EMAIL="your-email@gmail.com"
export SENDER_APP_PASSWORD="your-app-specific-password"

# Optional SMTP configuration (defaults to Gmail)
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
```

### Email Setup Guide

1. **Gmail Setup**: See [email_config.md](email_config.md) for detailed Gmail configuration instructions
2. **Test Email**: Run `python test_email_agent.py` to verify email functionality
3. **Default Recipient**: Reports are sent to recipients configured via GitHub secrets

### Email Features

- **Professional HTML Formatting**: Reports are converted to beautiful HTML emails
- **MCP Compatibility**: Uses Model Context Protocol standards
- **Automatic Delivery**: Integrated into the main workflow
- **Error Handling**: Graceful failure with detailed error messages
- **Security**: Uses app-specific passwords and TLS encryption

## Usage Examples

### Sample Queries
- "What are the latest AI agent trends?"
- "Find recent developments in multi-agent systems"
- "What new AI agent frameworks were released this week?"
- "Summarize recent research papers on AI agents"

### Expected Output Format
The agent generates structured reports with:

1. **Trend Summary** (3-5 major trends)
   - Trend description with evidence
   - Impact analysis
   - Relevant links and sources

2. **Recent Releases** (tools, frameworks, papers)
   - Name and description
   - Release date and significance
   - Links to documentation/repositories

3. **Developer Questions** (3-5 thought-provoking questions)
   - Strategic implications
   - Technical considerations
   - Future development opportunities

## Troubleshooting

### Common Issues

#### Model Access Errors (404 NOT_FOUND)
```
Error: Publisher Model `projects/.../gemini-1.5-pro` was not found
```
**Solution**: 
- Ensure Vertex AI API is enabled
- Verify your project has access to Gemini models
- Try a different region or model variant
- Check billing is enabled

#### Authentication Issues
```
Error: Could not automatically determine credentials
```
**Solution**:
```bash
gcloud auth application-default login
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```

#### Import Errors
```
ModuleNotFoundError: No module named 'trend_spotter'
```
**Solution**:
```bash
pip install -e .
# Ensure you're in the virtual environment
```

#### Web Interface Not Loading Agent
**Solution**:
- Remove any `.egg-info` directories: `rm -rf *.egg-info`
- Reinstall: `pip install -e . --force-reinstall`
- Ensure `__init__.py` exists and imports `root_agent`

### Validation Commands

```bash
# Check Google Cloud configuration
gcloud config list
gcloud auth application-default print-access-token

# Test Vertex AI access
python -c "from google.cloud import aiplatform; aiplatform.init(); print('Vertex AI OK')"

# Verify agent structure
python -c "from trend_spotter import root_agent; print(f'Agent: {root_agent.name}')"
```

## Development

### Customizing the Agent

- **Modify Search Strategy**: Edit `prompt.py` to change how the agent searches
- **Adjust Output Format**: Update the report structure in `prompt.py`
- **Change Model**: Update the `MODEL` variable in `agent.py`
- **Add Tools**: Import additional ADK tools in `agent.py`

### Testing

The project includes a comprehensive test suite with both unit and integration tests:

```bash
# Run all tests with pytest
pytest

# Run only unit tests (no external dependencies)
pytest -m unit

# Run integration tests (requires Google Cloud credentials)
pytest -m integration

# Run with verbose output
pytest -v

# Run specific test files
pytest tests/test_unit.py
pytest tests/test_integration.py

# Run standalone test scripts
python test_agent_functionality.py
python test_vertex_ai.py
```

#### Test Configuration
- **Unit Tests**: Test agent logic without external API calls
- **Integration Tests**: Test full functionality with Google Cloud services
- **Code Coverage**: Tracks test coverage across the codebase
- **Test Markers**: Organized by type (unit, integration, slow)

### Code Quality

The project maintains high code quality with automated formatting and linting:

```bash
# Format code with Black (line length: 79)
black .

# Sort imports with isort
isort .

# Lint with flake8
flake8 .

# Type checking with mypy
mypy trend_spotter

# Security scanning with bandit
bandit -r trend_spotter

# Check dependencies for vulnerabilities
safety check
```

#### Quality Standards
- **Line Length**: 79 characters (PEP 8 compliant)
- **Import Sorting**: Alphabetical with Black profile
- **Type Hints**: Enforced where possible
- **Security**: Regular vulnerability scanning
- **Documentation**: Comprehensive docstrings

## Deployment

The project supports automated deployment to Google Cloud Run with comprehensive CI/CD pipelines.

### Local Deployment

```bash
# Quick deployment using the deployment script
./deploy.sh

# Or manual deployment
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"
source myenv/bin/activate
adk deploy cloud_run \
  --project=$GOOGLE_CLOUD_PROJECT \
  --region=$GOOGLE_CLOUD_LOCATION \
  --service_name=trend-spotter-service \
  --app_name=trend-spotter-app \
  --with_ui \
  ./trend_spotter
```

### GitHub Actions Deployment

Automated deployment is configured with GitHub Actions workflows:

1. **CI/CD Pipeline** (`ci.yml`): Comprehensive testing, building, and deployment
2. **ADK Deployment** (`deploy-adk.yml`): Dedicated ADK agent deployment to Cloud Run
3. **Code Quality** (`code-quality.yml`): Automated code quality checks on PRs

#### Required Secrets

Set up these GitHub repository secrets for automated deployment:

- `GCP_SERVICE_ACCOUNT_KEY`: JSON key for Google Cloud service account
- `GOOGLE_CLOUD_PROJECT`: Your GCP project ID
- `GOOGLE_CLOUD_LOCATION`: Deployment region (optional, defaults to us-central1)
- `SERVICE_NAME`: Cloud Run service name (optional)
- `APP_NAME`: ADK app name (optional)

See [GITHUB_SECRETS_SETUP.md](GITHUB_SECRETS_SETUP.md) for detailed setup instructions.

#### Deployment Features

- **Automatic Triggers**: Deploy on push to main branch or manual trigger
- **Environment Management**: Support for multiple deployment environments
- **Security**: Uses service accounts with least privilege
- **Monitoring**: Includes health checks and deployment verification
- **UI Access**: Deploys with ADK Development UI enabled

### Deployment Documentation

- **[DEPLOYMENT.md](DEPLOYMENT.md)**: Comprehensive deployment guide
- **[GITHUB_SECRETS_SETUP.md](GITHUB_SECRETS_SETUP.md)**: GitHub Actions setup
- **[.github/workflows/README.md](.github/workflows/README.md)**: Workflow documentation

## CI/CD Pipeline

The project includes a robust CI/CD pipeline with multiple workflow configurations:

### Continuous Integration Features

- **Multi-Python Version Testing**: Tests against Python 3.9, 3.10, 3.11
- **Code Quality Checks**: Black formatting, isort import sorting, flake8 linting
- **Type Checking**: mypy static analysis
- **Security Scanning**: bandit security linting, safety dependency checks
- **Test Coverage**: pytest with coverage reporting
- **Build Verification**: Package building and installation testing
- **Integration Testing**: Full ADK agent functionality tests

### Automated Workflows

1. **Pull Request Checks**: Run on all PRs to ensure code quality
2. **Main Branch CI**: Full test suite and deployment on main branch updates
3. **Dependency Updates**: Automated Dependabot configuration for security updates
4. **Manual Deployment**: On-demand deployment with environment selection

### Workflow Triggers

- **Push to main**: Full CI/CD pipeline with deployment
- **Pull requests**: Code quality and testing workflows
- **Manual dispatch**: Deploy to specific environments
- **Schedule**: Regular dependency and security scans

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

[Specify your license here]

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review Google ADK documentation
3. Check Vertex AI status and quotas
4. Create an issue in the repository

---

**Note**: This project requires active Google Cloud billing and API access. Ensure you understand the pricing for Vertex AI model usage before running extensive queries.

