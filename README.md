# Q360 Agentic AI Test Platform

AI-powered test case and test data generation from Jira stories using Gemini API and LangGraph orchestration.

## Architecture

```
Jira Story → Test Case Generator Agent → Test Data Generator Agent → API Response
```

## Setup

### Prerequisites
- Python 3.10+
- Gemini API key
- Jira instance with API access

### Installation

1. **Clone/Navigate to project:**
   ```bash
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

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add:
   - `GEMINI_API_KEY`: Get from [Google AI Studio](https://aistudio.google.com/apikey)
   - `JIRA_URL`: Your Jira instance URL
   - `JIRA_EMAIL`: Your Jira email
   - `JIRA_API_TOKEN`: Get from Jira account settings

### Getting API Keys

#### Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Click "Create API key"
3. Copy and paste in `.env`

#### Jira API Token
1. Go to [Atlassian Account Settings](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Create API token
3. Copy and paste in `.env`

## Usage

### Start the API Server

```bash
python api/main.py
```

Server runs at `http://localhost:8000`

### API Endpoints

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Generate Test Cases & Data
```bash
curl -X POST http://localhost:8000/generate-tests \
  -H "Content-Type: application/json" \
  -d '{"jira_issue_key": "PROJ-123"}'
```

**Response:**
```json
{
  "jira_issue_key": "PROJ-123",
  "story_summary": "User should be able to login",
  "test_cases": [
    {
      "test_id": "TC_001",
      "title": "Valid login with correct credentials",
      "description": "User logs in with valid email and password",
      "steps": ["1. Enter email", "2. Enter password", "3. Click login"],
      "expected_result": "User is logged in successfully",
      "test_type": "positive",
      "priority": "high"
    }
  ],
  "test_data": [
    {
      "field_name": "email",
      "data_type": "email",
      "sample_value": "user@example.com",
      "constraints": "Must be valid email format",
      "test_category": "valid"
    }
  ],
  "error": ""
}
```

## Project Structure

```
qa-healthcare-agent/
├── agents/                 # AI Agents
│   ├── test_case_generator.py
│   └── test_data_generator.py
├── integrations/          # External integrations
│   └── jira_client.py
├── orchestrator/          # Workflow orchestration
│   └── workflow.py
├── api/                   # FastAPI backend
│   └── main.py
├── .env.example
├── requirements.txt
└── README.md
```

## How It Works

1. **Fetch Jira Story**: Retrieves story summary, description, and acceptance criteria from Jira
2. **Generate Test Cases**: Uses Gemini to create positive, negative, and edge case test cases
3. **Generate Test Data**: Creates test data for each test case (valid, invalid, boundary values)
4. **Return Results**: API returns structured test cases and test data

## Next Steps

- [ ] Add qTest integration for storing test cases
- [ ] Build React dashboard UI
- [ ] Add Script Generator agent (Selenium/RestAssured)
- [ ] Implement Deduplication agent
- [ ] Add Self-Healing agent
- [ ] Build Analytics agent
- [ ] Add execution engine
- [ ] Implement approval workflow (HITL)

## Troubleshooting

### Gemini API Key Error
- Ensure API key is valid and enabled in Google Cloud
- Check `.env` file has `GEMINI_API_KEY` set

### Jira Connection Error
- Verify Jira URL, email, and API token are correct
- Ensure Jira instance is accessible
- Check API token is generated and not expired

### JSON Parsing Error
- LLM response format might not be parseable
- Check Gemini API response in logs
- May need to refine prompts for consistency

## License

TBD
