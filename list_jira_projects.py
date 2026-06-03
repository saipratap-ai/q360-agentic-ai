"""
List all available Jira projects.
"""

import os
from dotenv import load_dotenv
from integrations.jira_client import JiraClient

# Load environment variables
load_dotenv()

jira_url = os.getenv("JIRA_URL")
jira_email = os.getenv("JIRA_EMAIL")
jira_api_token = os.getenv("JIRA_API_TOKEN")

print("=" * 60)
print("Available Jira Projects")
print("=" * 60)

try:
    jira_client = JiraClient(jira_url, jira_email, jira_api_token)

    # Get all projects
    projects = jira_client.jira.projects()

    if not projects:
        print("\n[INFO] No projects found")
    else:
        print(f"\n[INFO] Found {len(projects)} project(s):\n")
        for proj in projects:
            print(f"  Project Key: {proj.key}")
            print(f"  Project Name: {proj.name}")
            print(f"  Project Type: {proj.projectTypeKey}")
            print()

        # Suggestion
        print("=" * 60)
        print(f"Use one of these keys to create sample stories")
        print("=" * 60)

except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()
