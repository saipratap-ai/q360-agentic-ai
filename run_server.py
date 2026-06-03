"""
Q360 Standalone Server - Runs all API endpoints directly.
This avoids uvicorn module caching issues with api.main
"""
import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Load env vars
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Initialize app
app = FastAPI(title="Q360 Agentic AI Test Platform", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== INITIALIZE CLIENTS =====
from api.secrets import init_secrets, get_jira_credentials
from integrations.jira_client import JiraClient
from orchestrator.workflow import Q360Workflow

project_id = os.getenv("GCP_PROJECT_ID", "gen-lang-client-0256721605")
try:
    init_secrets(project_id)
    jira_url, jira_email, jira_token = get_jira_credentials()
except Exception as e:
    print(f"[WARN] Secret Manager failed: {e}")
    jira_url = os.getenv("JIRA_URL")
    jira_email = os.getenv("JIRA_EMAIL")
    jira_token = os.getenv("JIRA_API_TOKEN")

jira_client = None
try:
    jira_client = JiraClient(jira_url, jira_email, jira_token)
    print("[OK] Jira client initialized")
except Exception as e:
    print(f"[WARN] Jira client failed: {e}")

workflow = None
try:
    workflow = Q360Workflow(
        gcp_project_id=project_id,
        gcp_region=os.getenv("GCP_REGION", "us-central1"),
        jira_url=jira_url,
        jira_email=jira_email,
        jira_api_token=jira_token,
    )
    print("[OK] Q360Workflow initialized")
except Exception as e:
    print(f"[WARN] Workflow failed: {e}")


class GenerateTestsRequest(BaseModel):
    jira_issue_key: str


# ===== API ENDPOINTS =====

@app.get("/health")
async def health():
    return {"status": "ok", "jira": jira_client is not None, "workflow": workflow is not None}


@app.get("/api/jira/projects")
async def list_projects():
    """Get all Jira projects - REAL DATA"""
    if not jira_client:
        raise HTTPException(503, "Jira client not initialized")
    try:
        projects = jira_client.get_projects()
        return {"projects": projects}
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")


@app.get("/api/jira/issues")
async def list_issues(project: str):
    """Get issues from a Jira project - REAL DATA"""
    if not jira_client:
        raise HTTPException(503, "Jira client not initialized")
    try:
        issues = jira_client.get_issues_by_project(project, max_results=30)
        return {"issues": issues}
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")


@app.post("/api/generate-tests/stream")
async def generate_tests_stream(request: GenerateTestsRequest):
    """Generate tests with streaming - REAL AI DATA"""
    if not workflow:
        raise HTTPException(503, "Workflow not initialized")

    async def event_generator():
        try:
            yield f"data: {json.dumps({'type': 'status', 'message': 'Connecting to Jira...'})}\n\n"
            yield f"data: {json.dumps({'type': 'status', 'message': 'Fetching story details...'})}\n\n"

            result = workflow.execute(request.jira_issue_key)

            if result.get("error"):
                yield f"data: {json.dumps({'type': 'error', 'message': result['error']})}\n\n"
            else:
                yield f"data: {json.dumps({'type': 'story', 'data': {'key': result.get('jira_issue_key'), 'summary': result.get('story_summary')}})}\n\n"

                test_cases = result.get('test_cases', [])
                for i, tc in enumerate(test_cases, 1):
                    yield f"data: {json.dumps({'type': 'progress', 'message': f'Generated test case {i}/{len(test_cases)}'})}\n\n"
                    yield f"data: {json.dumps({'type': 'test_case', 'data': tc})}\n\n"

                test_data = result.get('test_data', [])
                for i, td in enumerate(test_data, 1):
                    yield f"data: {json.dumps({'type': 'progress', 'message': f'Generated test data {i}/{len(test_data)}'})}\n\n"
                    yield f"data: {json.dumps({'type': 'test_data', 'data': td})}\n\n"

                yield f"data: {json.dumps({'type': 'complete', 'message': 'Test generation complete!'})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.get("/api/info")
async def api_info():
    return {
        "name": "Q360 Agentic AI Test Platform",
        "version": "1.0.0",
        "jira_connected": jira_client is not None,
        "workflow_ready": workflow is not None,
    }


@app.get("/")
async def root():
    frontend_path = Path(__file__).parent / "frontend" / "build" / "index.html"
    if frontend_path.exists():
        return FileResponse(frontend_path)
    return {"message": "Q360 API running. Frontend at /frontend/build/"}


# Static files
frontend_static = Path(__file__).parent / "frontend" / "build" / "static"
if frontend_static.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_static)), name="static")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", os.getenv("API_PORT", 8000)))
    print(f"\n[Q360] Starting server on http://localhost:{port}")
    print(f"[Q360] Routes: {[r.path for r in app.routes]}\n")
    uvicorn.run(app, host="0.0.0.0", port=port)
