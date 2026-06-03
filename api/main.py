from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from orchestrator.workflow import Q360Workflow
from integrations.jira_client import JiraClient
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

# Initialize Jira client
jira_client = None
try:
    jira_client = JiraClient(jira_url, jira_email, jira_token)
    print("[INFO] Jira client initialized successfully")
except Exception as e:
    print(f"[WARNING] Failed to initialize Jira client: {e}")

# Initialize workflow with Google Cloud configuration
workflow = None
try:
    workflow = Q360Workflow(
        gcp_project_id=project_id,
        gcp_region=os.getenv("GCP_REGION", "us-central1"),
        jira_url=jira_url,
        jira_email=jira_email,
        jira_api_token=jira_token,
    )
    print("[INFO] Q360Workflow initialized successfully")
except Exception as e:
    print(f"[WARNING] Failed to initialize workflow: {e}")
    print("[INFO] App will start but generate-tests endpoint will fail until workflow is ready")


class GenerateTestsRequest(BaseModel):
    jira_issue_key: str


class GenerateTestsResponse(BaseModel):
    jira_issue_key: str
    story_summary: str
    test_cases: list
    test_data: list
    error: str


# Define API routes BEFORE mounting static files
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/api/jira/projects")
async def list_projects():
    """Get all accessible Jira projects."""
    if jira_client is None:
        raise HTTPException(
            status_code=503,
            detail="Jira client not initialized"
        )

    try:
        projects = jira_client.get_projects()
        return {"projects": projects}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching projects: {str(e)}"
        )


@app.get("/api/jira/issues")
async def list_issues(project: str):
    """Get issues from a specific Jira project."""
    if jira_client is None:
        raise HTTPException(
            status_code=503,
            detail="Jira client not initialized"
        )

    try:
        issues = jira_client.get_issues_by_project(project, max_results=30)
        return {"issues": issues}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching issues: {str(e)}"
        )


@app.post("/generate-tests", response_model=GenerateTestsResponse)
async def generate_tests(request: GenerateTestsRequest):
    """
    Generate test cases and test data for a Jira issue.

    Args:
        request: GenerateTestsRequest with jira_issue_key

    Returns:
        GenerateTestsResponse with test cases and test data
    """
    if workflow is None:
        raise HTTPException(
            status_code=503,
            detail="Workflow not initialized. Please check server logs and try again."
        )

    try:
        result = workflow.execute(request.jira_issue_key)

        if result.get("error"):
            raise HTTPException(status_code=400, detail=result["error"])

        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating tests: {str(e)}"
        )


@app.post("/api/generate-tests/stream")
async def generate_tests_stream(request: GenerateTestsRequest):
    """
    Generate test cases and test data with streaming progress updates.

    Uses Server-Sent Events (SSE) to stream updates as tests are generated.
    """
    if workflow is None:
        raise HTTPException(
            status_code=503,
            detail="Workflow not initialized. Please check server logs and try again."
        )

    async def event_generator():
        try:
            yield f"data: {json.dumps({'type': 'status', 'message': 'Starting test generation...'})}\n\n"

            # Execute workflow
            result = workflow.execute(request.jira_issue_key)

            if result.get("error"):
                yield f"data: {json.dumps({'type': 'error', 'message': result['error']})}\n\n"
            else:
                # Send story info
                yield f"data: {json.dumps({'type': 'story', 'data': {'key': result.get('jira_issue_key'), 'summary': result.get('story_summary')}})}\n\n"

                # Send test cases with progress
                test_cases = result.get('test_cases', [])
                total = len(test_cases)
                for i, tc in enumerate(test_cases, 1):
                    yield f"data: {json.dumps({'type': 'progress', 'current': i, 'total': total, 'message': f'Generated test case {i}/{total}'})}\n\n"
                    yield f"data: {json.dumps({'type': 'test_case', 'data': tc})}\n\n"

                # Send test data
                test_data = result.get('test_data', [])
                total = len(test_data)
                for i, td in enumerate(test_data, 1):
                    yield f"data: {json.dumps({'type': 'progress', 'current': i, 'total': total, 'message': f'Generated test data {i}/{total}'})}\n\n"
                    yield f"data: {json.dumps({'type': 'test_data', 'data': td})}\n\n"

                # Send completion
                yield f"data: {json.dumps({'type': 'complete', 'message': 'Test generation complete!'})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': f'Error: {str(e)}'})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.get("/api/info")
async def api_info():
    """API information endpoint."""
    return {
        "name": "Q360 Agentic AI Test Platform",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "generate_tests": "/generate-tests",
            "api_info": "/api/info",
        },
    }


@app.get("/")
async def root_redirect():
    """Serve the React frontend."""
    from fastapi.responses import FileResponse
    frontend_path = Path(__file__).parent.parent / "frontend" / "build" / "index.html"
    if frontend_path.exists():
        return FileResponse(frontend_path)
    return {"message": "Q360 Frontend - React app ready"}


# Serve static files for JS/CSS bundles
frontend_path = Path(__file__).parent.parent / "frontend" / "build"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path / "static")), name="static")


if __name__ == "__main__":
    import uvicorn

    # Cloud Run sets PORT environment variable, defaulting to 8080
    # For local development, API_PORT can be used
    port = int(os.getenv("PORT", os.getenv("API_PORT", 8000)))

    uvicorn.run(
        app,
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=port,
    )
