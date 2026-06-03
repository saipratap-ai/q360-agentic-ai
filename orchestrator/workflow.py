from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Any, Dict
from agents.google_cloud_agent_factory import GoogleCloudAgentFactory
from integrations.jira_client import JiraClient


class WorkflowState(TypedDict):
    """State passed through the workflow."""

    jira_story: Dict
    test_cases: List
    test_data: List
    error: str


class Q360Workflow:
    def __init__(
        self,
        gcp_project_id: str,
        gcp_region: str,
        jira_url: str,
        jira_email: str,
        jira_api_token: str,
    ):
        # Initialize Google Cloud Agent Factory
        agent_factory = GoogleCloudAgentFactory(gcp_project_id, gcp_region)
        self.tc_generator = agent_factory.create_test_case_generator_agent()
        self.td_generator = agent_factory.create_test_data_generator_agent()

        # Initialize Jira client
        self.jira_client = JiraClient(jira_url, jira_email, jira_api_token)

        self.graph = self._build_graph()

    def _build_graph(self):
        """Build the LangGraph workflow."""
        graph = StateGraph(WorkflowState)

        # Add nodes
        graph.add_node("generate_test_cases", self._generate_test_cases)
        graph.add_node("generate_test_data", self._generate_test_data)

        # Add edges
        graph.add_edge("generate_test_cases", "generate_test_data")
        graph.add_edge("generate_test_data", END)

        # Set entry point
        graph.set_entry_point("generate_test_cases")

        return graph.compile()

    def _generate_test_cases(self, state: WorkflowState) -> WorkflowState:
        """Node: Generate test cases from Jira story."""
        try:
            story = state["jira_story"]

            test_cases = self.tc_generator.generate_test_cases(story)

            state["test_cases"] = [tc.model_dump() for tc in test_cases]
            state["error"] = ""
        except Exception as e:
            state["error"] = f"Error generating test cases: {str(e)}"
            state["test_cases"] = []

        return state

    def _generate_test_data(self, state: WorkflowState) -> WorkflowState:
        """Node: Generate test data for test cases."""
        try:
            if not state["test_cases"]:
                state["test_data"] = []
                return state

            story_context = state["jira_story"].get("summary", "")
            test_cases = state["test_cases"]

            test_data = self.td_generator.generate_test_data(test_cases, story_context)

            state["test_data"] = [td.model_dump() for td in test_data]
        except Exception as e:
            state["error"] = f"Error generating test data: {str(e)}"
            state["test_data"] = []

        return state

    def execute(self, jira_issue_key: str) -> dict:
        """
        Execute the workflow for a Jira issue.

        Args:
            jira_issue_key: Jira issue key (e.g., 'PROJ-123')

        Returns:
            dict with test_cases and test_data
        """
        # Fetch the story from Jira
        story = self.jira_client.fetch_story(jira_issue_key)

        if not story:
            return {"error": f"Could not fetch story {jira_issue_key}"}

        # Initialize workflow state
        initial_state = {
            "jira_story": story,
            "test_cases": [],
            "test_data": [],
            "error": "",
        }

        # Execute the workflow
        result = self.graph.invoke(initial_state)

        return {
            "jira_issue_key": jira_issue_key,
            "story_summary": story.get("summary", ""),
            "test_cases": result["test_cases"],
            "test_data": result["test_data"],
            "error": result.get("error", ""),
        }
