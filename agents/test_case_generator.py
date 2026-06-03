import json
import google.generativeai as genai
from typing import List
from pydantic import BaseModel


class TestCase(BaseModel):
    test_id: str
    title: str
    description: str
    steps: List[str]
    expected_result: str
    test_type: str  # positive, negative, edge
    priority: str  # high, medium, low


class TestCaseGeneratorAgent:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    def generate_test_cases(self, story: dict) -> list[TestCase]:
        """
        Generate test cases from Jira story.

        Args:
            story: Dict with keys: summary, description, acceptance_criteria

        Returns:
            List of TestCase objects
        """
        prompt = self._build_prompt(story)

        response = self.model.generate_content(prompt)

        # Parse the response
        test_cases = self._parse_response(response.text)

        return test_cases

    def _build_prompt(self, story: dict) -> str:
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

    def _parse_response(self, response_text: str) -> list[TestCase]:
        """Extract JSON from response and convert to TestCase objects."""
        try:
            # Try to find JSON array in the response
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1

            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON array found in response")

            json_str = response_text[start_idx:end_idx]
            test_cases_data = json.loads(json_str)

            test_cases = [TestCase(**tc) for tc in test_cases_data]
            return test_cases
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error parsing response: {e}")
            return []
