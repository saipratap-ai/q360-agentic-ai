"""
Create sample Jira stories for testing Q360 agents.
"""

import os
from dotenv import load_dotenv
from integrations.jira_client import JiraClient

# Load environment variables
load_dotenv()

jira_url = os.getenv("JIRA_URL")
jira_email = os.getenv("JIRA_EMAIL")
jira_api_token = os.getenv("JIRA_API_TOKEN")

print("=" * 70)
print("Creating Sample Jira Stories for Q360 Testing")
print("=" * 70)

if not jira_url or not jira_email or not jira_api_token:
    print("\n[ERROR] Missing Jira credentials in .env file")
    exit(1)

# Initialize Jira client
try:
    jira_client = JiraClient(jira_url, jira_email, jira_api_token)
    print("\n[SUCCESS] Connected to Jira")
except Exception as e:
    print(f"\n[ERROR] Failed to connect to Jira: {e}")
    exit(1)

# Ask for project key
project_key = input("\nEnter Jira Project Key (e.g., QA, TEST, PROJ): ").strip().upper()

if not project_key:
    print("[ERROR] Project key is required")
    exit(1)

# Sample stories for testing
sample_stories = [
    {
        "summary": "User Registration with Email Validation",
        "description": """As a new user, I want to register for an account with email and password so that I can access the platform.

Acceptance Criteria:
- User should be able to enter email and password
- Email must be in valid format (user@domain.com)
- Password must be at least 8 characters long
- Password must contain at least one uppercase, one lowercase, and one number
- User should receive a confirmation email with verification link
- System should prevent duplicate email registration with clear error message
- Registration form should validate all fields before submission
- Successful registration should redirect to login page""",
        "issue_type": "Story",
    },
    {
        "summary": "User Login Functionality",
        "description": """As a registered user, I want to login with my email and password so that I can access my account.

Acceptance Criteria:
- User should be able to enter email and password on login page
- System should validate credentials against database
- Invalid credentials should show clear error message
- Password field should mask the input for security
- "Remember Me" checkbox should persist login session for 30 days
- Failed login attempts should be logged for security audit
- After 5 failed attempts, account should be locked for 15 minutes
- Login should redirect to dashboard on success""",
        "issue_type": "Story",
    },
    {
        "summary": "Export Test Results to Excel",
        "description": """As a QA manager, I want to export test results to Excel so that I can share reports with stakeholders.

Acceptance Criteria:
- User should be able to select test results from dashboard
- Export should include test case ID, name, status, duration, and error details
- Excel file should have proper formatting with headers and borders
- Large datasets (10k+ rows) should export without performance issues
- Export should support filtering by date range and test status
- File name should include export date and time
- Email notification should be sent after export completes
- Exported file should be downloadable from a secure link""",
        "issue_type": "Story",
    },
    {
        "summary": "Search Test Cases by Keywords",
        "description": """As a QA engineer, I want to search test cases by keywords so that I can find relevant tests quickly.

Acceptance Criteria:
- Search should support keyword matching in test title and description
- Results should be sorted by relevance (title matches first)
- Search should support filters: status, priority, author, date range
- Search results should show total count and pagination
- Quick search should return results within 2 seconds
- Search should support advanced query syntax (AND, OR, NOT)
- Search history should be saved for quick access
- Saved searches should be shareable with team members""",
        "issue_type": "Story",
    },
    {
        "summary": "Automated Test Execution Report",
        "description": """As a DevOps engineer, I want automated test execution reports so that I can track quality metrics in CI/CD pipeline.

Acceptance Criteria:
- Report should be generated after each test execution run
- Report should include: total tests, passed, failed, skipped counts
- Report should show execution time and performance metrics
- Failed tests should include stack traces and error logs
- Report should identify flaky tests (tests that pass/fail inconsistently)
- Summary report should be sent to Slack/Email automatically
- Historical trend data should show quality improvements over time
- Report should be downloadable in PDF and HTML formats""",
        "issue_type": "Story",
    },
]

print(f"\n[INFO] Creating {len(sample_stories)} sample stories in project: {project_key}\n")

created_issues = []

for i, story in enumerate(sample_stories, 1):
    print(f"[{i}/{len(sample_stories)}] Creating: {story['summary']}")

    result = jira_client.create_issue(
        project_key=project_key,
        summary=story["summary"],
        description=story["description"],
        issue_type=story["issue_type"],
    )

    if result:
        created_issues.append(result)
        print(f"         Created: {result['key']}")
    else:
        print(f"         [ERROR] Failed to create issue")

print("\n" + "=" * 70)
print(f"[SUCCESS] Created {len(created_issues)} sample stories!")
print("=" * 70)

print("\nCreated Issues:")
for issue in created_issues:
    print(f"  - {issue['key']}: {issue['summary']}")

print(f"\nNext steps:")
print(f"1. Go to your Jira project: {jira_url}/browse/{project_key}")
print(f"2. Use these issue keys to test Q360 test case generation")
print(f"3. Example: python test_jira_connection.py (then enter {created_issues[0]['key']})")
