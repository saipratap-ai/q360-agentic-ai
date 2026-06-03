from jira import JIRA
from typing import Dict, List, Optional


class JiraClient:
    def __init__(self, jira_url: str, email: str, api_token: str):
        """Initialize Jira client."""
        self.jira = JIRA(jira_url, basic_auth=(email, api_token))

    def fetch_story(self, issue_key: str) -> Dict:
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

    def fetch_stories_by_jql(self, jql_query: str, max_results: int = 10) -> List[Dict]:
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

    def get_projects(self) -> List[Dict]:
        """
        Get all accessible Jira projects.

        Returns:
            List of project dicts with key and name
        """
        try:
            projects = self.jira.projects()
            return [
                {
                    "key": p.key,
                    "name": p.name,
                    "type": p.projectTypeKey if hasattr(p, 'projectTypeKey') else 'software'
                }
                for p in projects
            ]
        except Exception as e:
            print(f"Error fetching projects: {e}")
            return []

    def get_issues_by_project(self, project_key: str, max_results: int = 20) -> List[Dict]:
        """
        Get recent issues from a project.

        Args:
            project_key: Project key (e.g., 'KAN')
            max_results: Maximum number of issues to return

        Returns:
            List of issue dicts with key, summary, and status
        """
        try:
            jql_query = f"project = {project_key} ORDER BY updated DESC"
            issues = self.jira.search_issues(jql_query, maxResults=max_results)
            return [
                {
                    "key": issue.key,
                    "summary": issue.fields.summary,
                    "status": issue.fields.status.name,
                    "type": issue.fields.issuetype.name
                }
                for issue in issues
            ]
        except Exception as e:
            print(f"Error fetching issues: {e}")
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

    def create_issue(self, project_key: str, summary: str, description: str, issue_type: str = "Story") -> Dict:
        """
        Create a new Jira issue.

        Args:
            project_key: Project key (e.g., 'PROJ')
            summary: Issue summary/title
            description: Issue description with acceptance criteria
            issue_type: Issue type (Story, Task, Bug, etc.)

        Returns:
            Dict with created issue details
        """
        try:
            issue_dict = {
                "project": {"key": project_key},
                "summary": summary,
                "description": description,
                "issuetype": {"name": issue_type},
            }

            created_issue = self.jira.create_issue(fields=issue_dict)

            return {
                "key": created_issue.key,
                "id": created_issue.id,
                "summary": summary,
                "status": "To Do",
            }
        except Exception as e:
            print(f"Error creating issue: {e}")
            return {}
