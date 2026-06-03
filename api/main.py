from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path
from dotenv import load_dotenv
from orchestrator.workflow import Q360Workflow
from api.secrets import init_secrets, get_jira_credentials, get_google_api_key

# Load environment variables (for local development)
load_dotenv()

app = FastAPI(title="Q360 Agentic AI Test Platform", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize secrets
project_id = os.getenv("GCP_PROJECT_ID", "gen-lang-client-0256721605")
try:
    init_secrets(project_id)
    jira_url, jira_email, jira_token = get_jira_credentials()
except Exception as e:
    print(f"Warning: Could not load secrets from Secret Manager: {e}")
    # Fallback to environment variables
    jira_url = os.getenv("JIRA_URL")
    jira_email = os.getenv("JIRA_EMAIL")
    jira_token = os.getenv("JIRA_API_TOKEN")

# Initialize workflow with Google Cloud configuration
workflow = Q360Workflow(
    gcp_project_id=project_id,
    gcp_region=os.getenv("GCP_REGION", "us-central1"),
    jira_url=jira_url,
    jira_email=jira_email,
    jira_api_token=jira_token,
)

# Serve frontend static files
frontend_path = Path(__file__).parent.parent / "frontend" / "build"
if frontend_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")


class GenerateTestsRequest(BaseModel):
    jira_issue_key: str


class GenerateTestsResponse(BaseModel):
    jira_issue_key: str
    story_summary: str
    test_cases: list
    test_data: list
    error: str


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/generate-tests", response_model=GenerateTestsResponse)
async def generate_tests(request: GenerateTestsRequest):
    """
    Generate test cases and test data for a Jira issue.

    Args:
        request: GenerateTestsRequest with jira_issue_key

    Returns:
        GenerateTestsResponse with test cases and test data
    """
    try:
        result = workflow.execute(request.jira_issue_key)

        if result.get("error"):
            raise HTTPException(status_code=400, detail=result["error"])

        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating tests: {str(e)}"
        )


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Q360 Agentic AI Test Platform",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "generate_tests": "/generate-tests",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
    )
