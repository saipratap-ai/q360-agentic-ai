"""
Google Cloud Agents SDK for creating and managing AI agents.
Factory for creating test case and test data generation agents.
"""

from typing import Dict, List, Any
import google.generativeai as genai
import json
import os


class GoogleCloudAgentFactory:
    """Factory for creating and managing Google Cloud Agents."""

    def __init__(self, project_id: str, region: str = "us-central1"):
        """
        Initialize Google Cloud Agent Factory.

        Args:
            project_id: Google Cloud project ID
            region: GCP region (default: us-central1)
        """
        self.project_id = project_id
        self.region = region

        # Initialize with API key from environment
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            # Try to get from gcloud auth
            from google.auth import default
            credentials, _ = default()
            genai.configure(credentials=credentials)
        else:
            genai.configure(api_key=api_key)

    def create_test_case_generator_agent(self) -> "TestCaseGeneratorAgent":
        """Create a test case generator agent using Google Cloud Agents."""
        return TestCaseGeneratorAgent(self.project_id, self.region)

    def create_test_data_generator_agent(self) -> "TestDataGeneratorAgent":
        """Create a test data generator agent using Google Cloud Agents."""
        return TestDataGeneratorAgent(self.project_id, self.region)


class TestCaseGeneratorAgent:
    """Test Case Generator Agent using Google Cloud Generative Models."""

    def __init__(self, project_id: str, region: str = "us-central1"):
        """Initialize Test Case Generator Agent."""
        self.project_id = project_id
        self.region = region
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def generate_test_cases(self, story: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Generate test cases from a Jira story using Vertex AI.

        Args:
            story: Dict with keys: summary, description, acceptance_criteria

        Returns:
            List of test case dictionaries
        """
        prompt = self._build_prompt(story)

        try:
            response = self.model.generate_content(prompt)
            test_cases = self._parse_response(response.text)
            return test_cases
        except Exception as e:
            print(f"Error generating test cases: {e}")
            return []

    def _build_prompt(self, story: Dict) -> str:
        return f"""
You are a QA test case generation expert. Generate comprehensive test cases from the following Jira story.

STORY SUMMARY: {story.get('summary', '')}

STORY DESCRIPTION: {story.get('description', '')}

ACCEPTANCE CRITERIA: {story.get('acceptance_criteria', '')}

Generate test cases covering:
1. Positive scenarios (happy path)
2. Negative scenarios (invalid inputs, error cases)
3. Edge cases (boundary conditions, special characters)

For each test case, provide:
- test_id (format: TC_001, TC_002, etc.)
- title (concise test case name)
- description (what is being tested)
- steps (numbered list of steps to execute)
- expected_result (what should happen)
- test_type (positive, negative, or edge)
- priority (high, medium, or low)

Return the response as a JSON array of test cases with this exact structure:
[
  {{
    "test_id": "TC_001",
    "title": "Test case title",
    "description": "What is being tested",
    "steps": ["Step 1", "Step 2", "Step 3"],
    "expected_result": "Expected outcome",
    "test_type": "positive",
    "priority": "high"
  }}
]

Generate at least 5 test cases (mix of positive, negative, and edge cases).
"""

    def _parse_response(self, response_text: str) -> List[Dict]:
        """Extract JSON from response."""
        try:
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1

            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON array found in response")

            json_str = response_text[start_idx:end_idx]
            test_cases = json.loads(json_str)
            return test_cases
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error parsing response: {e}")
            return []


class TestDataGeneratorAgent:
    """Test Data Generator Agent using Google Cloud Generative Models."""

    def __init__(self, project_id: str, region: str = "us-central1"):
        """Initialize Test Data Generator Agent."""
        self.project_id = project_id
        self.region = region
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def generate_test_data(self, test_cases: List, story_context: str) -> List[Dict]:
        """
        Generate test data for test cases using Vertex AI.

        Args:
            test_cases: List of test case objects
            story_context: Story summary/context

        Returns:
            List of test data dictionaries
        """
        prompt = self._build_prompt(test_cases, story_context)

        try:
            response = self.model.generate_content(prompt)
            test_data = self._parse_response(response.text)
            return test_data
        except Exception as e:
            print(f"Error generating test data: {e}")
            return []

    def _build_prompt(self, test_cases: List, story_context: str) -> str:
        test_cases_str = "\n".join(
            [f"- {tc.get('title', tc)}: {tc.get('description', '')}" for tc in test_cases]
        )

        return f"""
You are a QA test data generation expert. Generate comprehensive test data for the following test cases.

STORY CONTEXT: {story_context}

TEST CASES TO COVER:
{test_cases_str}

Generate test data that includes:
1. Valid data sets (happy path scenarios)
2. Invalid data sets (error cases, malformed inputs)
3. Boundary data sets (edge values, limits)

For each data point, provide:
- field_name (name of the input field or parameter)
- data_type (string, int, email, date, boolean, phone, URL, etc.)
- sample_value (actual test value)
- constraints (validation rules, format requirements)
- test_category (valid, invalid, or boundary)

Return the response as a JSON array of test data with this exact structure:
[
  {{
    "field_name": "email",
    "data_type": "email",
    "sample_value": "user@example.com",
    "constraints": "Must be valid email format",
    "test_category": "valid"
  }}
]

Include at least 10-15 diverse test data sets covering all fields, formats, and edge cases.
"""

    def _parse_response(self, response_text: str) -> List[Dict]:
        """Extract JSON from response."""
        try:
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1

            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON array found in response")

            json_str = response_text[start_idx:end_idx]
            test_data = json.loads(json_str)
            return test_data
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error parsing response: {e}")
            return []
