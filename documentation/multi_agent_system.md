# TrendSpotter Multi-Agent System Architecture

## Overview

TrendSpotter has evolved from a single agent to a sophisticated **multi-agent system** that leverages specialization and coordination to provide comprehensive AI trend analysis.

## Architecture Evolution

### Before: Single Agent
- Single `root_agent` handled all tasks
- Limited specialization
- Sequential processing
- Monolithic prompt structure

### After: Multi-Agent System
- **Orchestrator Agent**: Coordinates and synthesizes
- **Specialist Sub-Agents**: Domain-specific expertise
- **Parallel Processing**: Simultaneous research across sources
- **Modular Design**: Easy to extend and maintain

## Agent Hierarchy

```
TrendSpotterOrchestrator (LlmAgent)
├── Tools: Sub-agents wrapped in AgentTool
│   ├── Google Search Agent (Agent)
│   │   └── Tool: google_search
│   ├── Reddit Agent (Agent)
│   │   └── Tool: search_hot_reddit_posts
│   └── Email Agent (Agent)
│       └── Tool: send_email_report
```

## Agent Details

### 🎯 TrendSpotterOrchestrator

**Type**: `LlmAgent` (Language Learning Model Agent)
**Role**: Manager and coordinator
**Model**: `gemini-2.5-pro-preview-05-06`

**Responsibilities**:
- Coordinate research across multiple sources
- Synthesize information from sub-agents
- Filter content for developer relevance
- Generate structured intelligence reports
- Ensure quality and consistency

**Tools**: Sub-agents (via `AgentTool` wrapper)
- `google_search_agent`
- `reddit_agent`
- `email_agent`

### 🔍 Google Search Agent

**Type**: `Agent` (Standard Agent)
**Role**: Web research specialist
**Model**: `gemini-2.5-pro-preview-05-06`

**Responsibilities**:
- Execute Google searches for recent AI agent news
- Find framework updates (LangChain, ADK, CrewAI, LlamaIndex)
- Discover technical tutorials and articles
- Return structured search results

**Tools**: 
- `google_search` (ADK built-in tool)

**Output Format**:
```
---
Title: [Search result title]
Link: [Full URL]
Snippet: [Description text]
---
```

### 📱 Reddit Agent

**Type**: `Agent` (Standard Agent)
**Role**: Community insights specialist
**Model**: `gemini-2.5-pro-preview-05-06`

**Responsibilities**:
- Monitor hot posts on developer subreddits
- Capture real developer conversations
- Identify practical challenges and solutions
- Focus on hands-on implementation discussions

**Tools**:
- `search_hot_reddit_posts` (Custom tool)

**Target Subreddits**:
- LocalLLaMA
- MachineLearning 
- LangChain
- AI_Agents
- LLMDevs
- singularity

### 📧 Email Agent

**Type**: `Agent` (Standard Agent)
**Role**: Report delivery specialist
**Model**: `gemini-2.5-flash-preview-05-20`

**Responsibilities**:
- Send formatted trend reports via email
- Handle HTML email formatting with professional styling
- Support multiple recipients configuration
- Provide delivery status and error handling
- Extract date ranges from reports for subject lines

**Tools**:
- `send_email_report` (Custom MCP-style tool)

**Features**:
- Professional HTML email templates with CSS styling
- Support for Gmail SMTP and other providers
- Environment variable configuration for credentials
- Multiple recipient support via comma-separated list
- Automatic markdown-to-HTML conversion
- Delivery status tracking and error reporting

**Email Configuration**:
- `SENDER_EMAIL`: Sender's email address
- `SENDER_APP_PASSWORD`: App-specific password (for Gmail)
- `EMAIL_RECIPIENTS`: Comma-separated list of recipient emails
- `SMTP_SERVER`: SMTP server (default: smtp.gmail.com)
- `SMTP_PORT`: SMTP port (default: 587)

## Multi-Agent Workflow

### 1. Initialization Phase
The orchestrator agent receives a request and initializes the workflow.

### 2. Date Discovery
```
Orchestrator → Google Search Agent: "Find current date"
Google Search Agent → Returns: Current date information
```

### 3. Parallel Research Phase
```
Orchestrator ─┬→ Google Search Agent: "Search for AI agent news (last 7 days)"
              └→ Reddit Agent: "Find hot developer discussions"
              
Google Search Agent → Returns: Recent news, frameworks, tutorials
Reddit Agent → Returns: Hot posts from developer subreddits
```

### 4. Synthesis Phase
```
Orchestrator receives both inputs:
├── Web Search Results (structured)
└── Reddit Community Insights (hot posts)

Orchestrator processes:
├── Combines information
├── Filters for developer relevance  
├── Identifies cross-platform topics
├── Prioritizes by discussion volume
└── Generates final report
```

### 5. Report Generation
Structured output with three sections:
- 🔥 **Top 5 Trends** for Agent Developers
- 🚀 **Top 5 Releases** for Agent Developers  
- 🤔 **Top 5 Questions** from Agent Developers

### 6. Email Delivery (Optional)
```
Orchestrator → Email Agent: "Send this report via email"
Email Agent processes:
├── Extracts date range from report
├── Creates professional HTML email formatting
├── Sends to configured recipients
└── Returns delivery confirmation
```

## Technical Implementation

### File Structure
```
trend_spotter/
├── agent.py                    # Orchestrator definition
├── prompt.py                   # Orchestrator prompt
├── tools.py                    # Custom tools (Reddit)
└── sub_agents/
    ├── __init__.py
    ├── google_search_agent.py   # Google Search specialist
    ├── reddit_agent.py          # Reddit specialist
    └── email_agent.py           # Email delivery specialist
```

### Key Code Changes

#### agent.py
```python
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from .sub_agents.google_search_agent import google_search_agent
from .sub_agents.reddit_agent import reddit_agent
from .sub_agents.email_agent import email_agent

root_agent = LlmAgent(
    model="gemini-2.5-flash-preview-05-20",
    name="TrendSpotterOrchestrator",
    instruction=prompt.ORCHESTRATOR_PROMPT,
    tools=[
        AgentTool(agent=google_search_agent),
        AgentTool(agent=reddit_agent),
        AgentTool(agent=email_agent),
    ],
)
```

#### Sub-Agent Example
```python
from google.adk.agents import Agent
from google.adk.tools import google_search

google_search_agent = Agent(
    model="gemini-2.5-pro-preview-05-06",
    name="google_search_agent",
    description="Expert at structured Google searches",
    instruction=SEARCH_AGENT_PROMPT,
    tools=[google_search],
)
```

## Benefits of Multi-Agent Architecture

### 🎯 **Specialization**
- Each agent focuses on its domain expertise
- Optimized prompts for specific tasks
- Better quality outputs per domain

### ⚡ **Parallel Processing**
- Multiple research streams simultaneously
- Faster overall completion time
- Better resource utilization

### 🔧 **Modularity**
- Easy to test individual components
- Independent updates and maintenance
- Clear separation of concerns

### 📈 **Scalability**
- Simple to add new specialist agents
- Easy to extend to new data sources
- Modular prompt management

### 🛡️ **Quality Control**
- Orchestrator ensures consistency
- Centralized filtering and prioritization
- Standardized output formats

## Testing Multi-Agent System

### Unit Tests
```bash
# Test agent structure and configuration
pytest tests/test_unit.py::test_multi_agent_imports -v
pytest tests/test_unit.py::test_agent_configuration -v
pytest tests/test_unit.py::test_sub_agent_structure -v
```

### Integration Tests
```bash
# Test with real external services (requires credentials)
pytest tests/test_integration.py -v
```

### Running the System
```bash
# Start web interface
adk web

# Access at http://localhost:8080
# Test with sample query about AI agent trends
```

## Future Enhancements

### Potential New Sub-Agents
- **GitHub Agent**: Monitor repository activity and releases
- **Twitter Agent**: Track social media discussions
- **Academic Agent**: Search arXiv and research papers
- **Hacker News Agent**: Track tech community discussions
- **Calendar Agent**: Schedule and manage report delivery
- **Slack/Teams Agent**: Send reports to team channels

### Advanced Features
- **Memory System**: Persist insights across sessions
- **Trend Detection**: Historical analysis and pattern recognition
- **Custom Filters**: User-defined content preferences
- **Real-time Updates**: Continuous monitoring capabilities

## Migration Notes

For users upgrading from the single-agent version:

1. **Environment Variables**: Same requirements (Google Cloud, Reddit API)
   - **New**: Email configuration variables for email delivery feature
2. **Dependencies**: Same `requirements.txt` with added email support
3. **Configuration**: Same `pyproject.toml` agent discovery
4. **Interface**: Same web interface at `http://localhost:8080`
5. **Output Format**: Enhanced but compatible report structure
6. **New Feature**: Optional email delivery of reports

The multi-agent system is designed to be a drop-in replacement with enhanced capabilities.

