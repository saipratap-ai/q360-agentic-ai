from jira import JIRA
from typing import dict, list


class JiraClient:
    def __init__(self, jira_url: str, email: str, api_token: str):
        """Initialize Jira client."""
        self.jira = JIRA(jira_url, basic_auth=(email, api_token))

    def fetch_story(self, issue_key: str) -> dict:
        """
        Fetch a Jira story by issue key.

        Args:
            issue_key: Jira issue key (e.g., 'PROJ-123')

        Returns:
            Dict with story details
        """
        try:
            issue = self.jira.issue(issue_key)

            story = {
                "key": issue.key,
                "summary": issue.fields.summary,
                "description": issue.fields.description or "",
                "acceptance_criteria": self._extract_acceptance_criteria(issue),
                "status": issue.fields.status.name,
                "issue_type": issue.fields.issuetype.name,
            }

            return story
        except Exception as e:
            print(f"Error fetching story {issue_key}: {e}")
            return {}

    def fetch_stories_by_jql(self, jql_query: str, max_results: int = 10) -> list[dict]:
        """
        Fetch multiple stories using JQL query.

        Args:
            jql_query: JQL query string (e.g., 'project = PROJ AND status = "Ready for QA"')
            max_results: Maximum number of results to return

        Returns:
            List of story dicts
        """
        try:
            issues = self.jira.search_issues(jql_query, maxResults=max_results)

            stories = [
                {
                    "key": issue.key,
                    "summary": issue.fields.summary,
                    "description": issue.fields.description or "",
                    "acceptance_criteria": self._extract_acceptance_criteria(issue),
                    "status": issue.fields.status.name,
                    "issue_type": issue.fields.issuetype.name,
                }
                for issue in issues
            ]

            return stories
        except Exception as e:
            print(f"Error fetching stories with JQL: {e}")
            return []

    def _extract_acceptance_criteria(self, issue) -> str:
        """Extract acceptance criteria from issue description or custom fields."""
        # Try to get from custom field first (customize as per your Jira setup)
        if hasattr(issue.fields, "customfield_10000"):  # Adjust field ID as needed
            return issue.fields.customfield_10000 or ""

        # Otherwise, extract from description (look for "Acceptance Criteria:" section)
        description = issue.fields.description or ""
        if "Acceptance Criteria:" in description:
            return description.split("Acceptance Criteria:")[1].strip()

        return ""
