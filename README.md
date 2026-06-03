# Q360 - Agentic AI Test Management & Automation Platform

AI-powered test case and test data generation platform that automates the QA lifecycle — from Jira story analysis to test creation using multi-agent AI orchestration.

## Overview

Q360 leverages **Google Gemini 2.5 Flash**, **LangGraph** orchestration, and **Jira API** integration to automatically generate comprehensive test suites from user stories. The platform features a modern React dashboard with real-time streaming, enterprise-grade UI, and seamless CI/CD deployment on Google Cloud Run.

## Key Features

- **AI-Driven Test Generation** — Generates structured test cases (positive, negative, edge) from Jira stories with >90% effort reduction
- **Test Data Generation** — Context-aware test data with valid, invalid, and boundary values
- **Real-Time Streaming** — Server-Sent Events (SSE) for live progress as tests are generated
- **Jira Integration** — Live project/issue selection with real-time data from Jira API
- **Enterprise Dashboard** — Dark-themed, responsive UI with sidebar navigation, analytics, and role-based views
- **Data Source Indicators** — Green "LIVE DATA" / yellow "MOCK DATA" badges so you always know what's real
- **Mobile Responsive** — Full hamburger menu navigation on mobile/tablet
- **Cloud Native** — Multi-stage Docker build, deployed on Google Cloud Run with Secret Manager

## Architecture

```
                    +-------------------+
                    |   React Frontend  |
                    |   (Dashboard UI)  |
                    +--------+----------+
                             |
                    +--------v----------+
                    |   FastAPI Server   |
                    |   (SSE Streaming)  |
                    +--------+----------+
                             |
              +--------------+--------------+
              |                             |
    +---------v---------+      +-----------v-----------+
    |   Jira Client     |      |   LangGraph Workflow   |
    |   (python-jira)   |      |   (Orchestrator)       |
    +-------------------+      +-----------+-----------+
                                           |
                               +-----------+-----------+
                               |                       |
                    +----------v--------+  +-----------v----------+
                    | Test Case Agent   |  | Test Data Agent      |
                    | (Gemini 2.5 Flash)|  | (Gemini 2.5 Flash)   |
                    +-------------------+  +----------------------+
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, CSS3 (dark theme, glassmorphism) |
| Backend | FastAPI, Uvicorn, SSE streaming |
| AI/LLM | Google Gemini 2.5 Flash via Vertex AI |
| Orchestration | LangGraph (multi-agent workflow) |
| Integration | python-jira, Jira REST API |
| Secrets | Google Cloud Secret Manager |
| Deployment | Docker (multi-stage), Google Cloud Run |
| CI/CD | Google Cloud Build |

## Project Structure

```
qa-healthcare-agent/
├── agents/                    # AI Agents
│   ├── test_case_generator.py # Generates test cases from stories
│   └── test_data_generator.py # Generates test data for fields
├── api/                       # FastAPI backend
│   ├── main.py                # API routes & endpoints
│   └── secrets.py             # Google Secret Manager integration
├── frontend/                  # React dashboard
│   ├── src/
│   │   ├── App.js             # Main dashboard component
│   │   └── App.css            # Dark theme styles
│   └── build/                 # Production build
├── integrations/              # External integrations
│   └── jira_client.py         # Jira API client
├── orchestrator/              # Workflow orchestration
│   └── workflow.py            # LangGraph multi-agent workflow
├── run_server.py              # Standalone server (recommended)
├── Dockerfile                 # Multi-stage Docker build
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- Google Cloud project with Gemini API enabled
- Jira instance with API access

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-org/qa-healthcare-agent.git
   cd qa-healthcare-agent
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and configure:
   ```env
   GEMINI_API_KEY=your-gemini-api-key
   JIRA_URL=https://your-domain.atlassian.net
   JIRA_EMAIL=your-email@domain.com
   JIRA_API_TOKEN=your-jira-api-token
   GCP_PROJECT_ID=your-gcp-project-id
   ```

5. **Build the frontend:**
   ```bash
   cd frontend
   npm install
   npm run build
   cd ..
   ```

6. **Start the backend:**
   ```bash
   python run_server.py
   ```

   Server runs at `http://localhost:8000`

7. **Open the dashboard:**
   
   Navigate to `http://localhost:8000` in your browser.

### API Keys

| Key | Where to Get |
|-----|-------------|
| Gemini API Key | [Google AI Studio](https://aistudio.google.com/apikey) |
| Jira API Token | [Atlassian Account Settings](https://id.atlassian.com/manage-profile/security/api-tokens) |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check (Jira & workflow status) |
| GET | `/api/jira/projects` | List all Jira projects |
| GET | `/api/jira/issues?project=KAN` | List issues from a project |
| POST | `/api/generate-tests/stream` | Generate tests with SSE streaming |
| POST | `/generate-tests` | Generate tests (non-streaming) |
| GET | `/api/info` | API info & integration status |

### Example: Generate Tests (Streaming)

```bash
curl -X POST http://localhost:8000/api/generate-tests/stream \
  -H "Content-Type: application/json" \
  -d '{"jira_issue_key": "KAN-10"}'
```

**SSE Response:**
```
data: {"type": "status", "message": "Connecting to Jira..."}
data: {"type": "story", "data": {"key": "KAN-10", "summary": "User Login Feature"}}
data: {"type": "test_case", "data": {"test_id": "TC_001", "title": "Valid login", ...}}
data: {"type": "test_data", "data": {"field_name": "email", "sample_value": "user@test.com", ...}}
data: {"type": "complete", "message": "Test generation complete!"}
```

## Dashboard Pages

| Page | Status | Description |
|------|--------|-------------|
| Dashboard | MVP | Metrics, coverage rings, activity feed |
| Test Generation | MVP | Jira integration, AI generation, streaming results |
| Automation | Phase 2 | Selenium/Rest Assured script generation |
| Execution | Phase 2 | CI/CD pipeline integration |
| Analytics | Phase 2 | Test coverage, defect density insights |
| Traceability | Phase 2 | Requirement-to-defect mapping |
| Settings | Phase 2 | Integrations & user management |

## Deployment

### Google Cloud Run

```bash
# Build and push Docker image
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/q360

# Deploy to Cloud Run
gcloud run deploy q360 \
  --image gcr.io/YOUR_PROJECT_ID/q360 \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --timeout 300 \
  --set-env-vars GCP_PROJECT_ID=YOUR_PROJECT_ID
```

### Environment Variables (Cloud Run)

Secrets are managed via **Google Cloud Secret Manager**:
- `jira-url` — Jira instance URL
- `jira-email` — Jira account email
- `jira-api-token` — Jira API token
- `gemini-api-key` — Google Gemini API key

## How It Works

1. **User selects** a Jira project and issue from the dashboard
2. **Jira Client** fetches story details (summary, description, acceptance criteria)
3. **LangGraph Orchestrator** coordinates the AI agents:
   - **Test Case Generator Agent** — Creates positive, negative, and edge case tests
   - **Test Data Generator Agent** — Creates valid, invalid, and boundary test data
4. **SSE Stream** sends results to the frontend in real-time
5. **Dashboard** displays test cases in an interactive table with expandable details

## Troubleshooting

| Issue | Solution |
|-------|---------|
| Jira connection error | Verify JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN in `.env` |
| Gemini API error | Check GEMINI_API_KEY is valid and Vertex AI is enabled |
| Port already in use | Kill existing processes: `netstat -ano \| findstr :8000` |
| Frontend not loading | Run `npm run build` in `/frontend` directory |
| Docker build fails | Ensure Node 18+ and Python 3.11+ are available |

## Roadmap

- [x] AI-driven test case generation (Gemini 2.5 Flash)
- [x] Test data generation (valid/invalid/boundary)
- [x] Jira integration (projects, issues)
- [x] SSE streaming with real-time progress
- [x] Enterprise dashboard UI (dark theme)
- [x] Mobile responsive with hamburger menu
- [x] Cloud Run deployment with Secret Manager
- [x] Live/Mock data source indicators
- [ ] qTest integration for test management
- [ ] Selenium script generation agent
- [ ] Rest Assured API script generation
- [ ] Self-healing agent for failed scripts
- [ ] Analytics & performance insights
- [ ] Execution engine with CI/CD integration
- [ ] Human-in-the-loop approval workflow
- [ ] Deduplication agent (semantic similarity)
- [ ] End-to-end traceability matrix

## License

Proprietary - Internal Use Only

## Author

Built by QA Engineering Team | Q360 Platform
