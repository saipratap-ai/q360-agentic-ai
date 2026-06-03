# Q360 Platform - Quick Start Guide

## Prerequisites
- Python 3.10+
- Node.js 16+ (for React dashboard)
- Google Cloud Billing enabled
- Jira account with project access

## Setup

### 1. Backend Setup

```bash
# Navigate to project root
cd qa-healthcare-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

Edit `.env` file with:
```
GCP_PROJECT_ID=gen-lang-client-0256721605
GCP_REGION=us-central1
GOOGLE_API_KEY=<your_api_key>
JIRA_URL=https://saipratap.atlassian.net
JIRA_EMAIL=<your_email>
JIRA_API_TOKEN=<your_token>
```

### 3. Test Backend

```bash
# Test direct agents
python test_agents_direct.py

# Test full workflow with Jira
python test_workflow.py
# Enter issue key: KAN-4
```

### 4. Start Backend API Server

```bash
python api/main.py
# Runs on http://localhost:8000
```

### 5. Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start React development server
npm start
# Opens http://localhost:3000
```

## Testing the Full Application

1. **Backend running:** `http://localhost:8000`
   - Health check: `http://localhost:8000/health`
   - API docs: `http://localhost:8000/docs`

2. **Frontend running:** `http://localhost:3000`
   - Enter Jira issue key (e.g., KAN-4)
   - Click "Generate Tests"
   - View generated test cases and test data

## Available Test Stories

These Jira stories are ready for testing:
- **KAN-4:** User Registration with Email Validation
- **KAN-5:** User Login Functionality
- **KAN-6:** Export Test Results to Excel
- **KAN-7:** Search Test Cases by Keywords
- **KAN-8:** Automated Test Execution Report

## API Endpoints

### Generate Tests
```
POST /generate-tests
Body: { "jira_issue_key": "KAN-4" }
```

Response:
```json
{
  "jira_issue_key": "KAN-4",
  "story_summary": "...",
  "test_cases": [...],
  "test_data": [...],
  "error": ""
}
```

## Architecture

```
Jira Stories
    ↓
[Jira Integration]
    ↓
[LangGraph Orchestrator]
    ↓
[Google Cloud Agents]
├── Test Case Generator (Gemini 2.5 Flash)
└── Test Data Generator (Gemini 2.5 Flash)
    ↓
[FastAPI Backend]
    ↓
[React Dashboard]
```

## Troubleshooting

### API Key Issues
- Verify API key in `.env`
- Check billing is enabled
- Ensure proper scopes

### Jira Connection Issues
- Verify credentials in `.env`
- Check Jira project exists (KAN)
- Ensure API token is valid

### CORS Issues
- Backend is configured to allow all origins (localhost:3000)
- Check backend is running on port 8000

## Next Steps

1. Deploy backend to cloud (Heroku, Google Cloud Run, etc.)
2. Build and deploy React frontend
3. Add more agents (Script Generator, Self-Healing, etc.)
4. Integrate with CI/CD pipelines
5. Add analytics dashboard

## Support

For issues or questions, check:
- GitHub: https://github.com/saipratap-ai/q360-agentic-ai
- Test results: `results_*.json` files
