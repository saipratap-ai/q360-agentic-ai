"""
Test Jira connection without requiring Gemini API quota.
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
print("Testing Jira Connection")
print("=" * 60)

# Check if credentials are set
if not jira_url or not jira_email or not jira_api_token:
    print("\n[ERROR] Missing Jira credentials in .env file")
    print("\nRequired:")
    print("  - JIRA_URL")
    print("  - JIRA_EMAIL")
    print("  - JIRA_API_TOKEN")
    exit(1)

print(f"\n[INFO] Jira URL: {jira_url}")
print(f"[INFO] Jira Email: {jira_email}")

# Try to connect
try:
    print("\n[CONNECTING] Attempting to connect to Jira...")
    jira_client = JiraClient(jira_url, jira_email, jira_api_token)

    print("[SUCCESS] Connected to Jira!")

    # Try to fetch a specific issue
    issue_key = input("\nEnter Jira issue key to test (e.g., PROJ-1): ").strip()

    if not issue_key:
        print("[INFO] Skipping issue fetch (no key provided)")
    else:
        print(f"\n[FETCHING] Getting issue: {issue_key}")
        story = jira_client.fetch_story(issue_key)

        if story:
            print(f"\n[SUCCESS] Issue fetched!\n")
            print(f"Key: {story.get('key')}")
            print(f"Summary: {story.get('summary')}")
            print(f"Type: {story.get('issue_type')}")
            print(f"Status: {story.get('status')}")
            print(f"\nDescription:\n{story.get('description')}")
            print(f"\nAcceptance Criteria:\n{story.get('acceptance_criteria')}")
        else:
            print(f"[ERROR] Could not fetch issue {issue_key}")

except Exception as e:
    print(f"\n[ERROR] Jira connection failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n" + "=" * 60)
print("[SUCCESS] Jira integration is working!")
print("=" * 60)
