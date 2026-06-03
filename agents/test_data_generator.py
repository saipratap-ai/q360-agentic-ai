import json
import google.generativeai as genai
from typing import list
from pydantic import BaseModel


class TestData(BaseModel):
    field_name: str
    data_type: str  # string, int, email, date, boolean, etc.
    sample_value: str
    constraints: str
    test_category: str  # valid, invalid, boundary


class TestDataGeneratorAgent:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-pro")

    def generate_test_data(self, test_cases: list, story_context: str) -> list[TestData]:
        """
        Generate test data for given test cases.

        Args:
            test_cases: List of test case objects with steps and descriptions
            story_context: Additional context from the Jira story

        Returns:
            List of TestData objects with various test datasets
        """
        prompt = self._build_prompt(test_cases, story_context)

        response = self.model.generate_content(prompt)

        # Parse the response
        test_data = self._parse_response(response.text)

        return test_data

    def _build_prompt(self, test_cases: list, story_context: str) -> str:
        test_cases_str = "\n".join(
            [f"- {tc.title}: {tc.description}" for tc in test_cases]
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
  }},
  {{
    "field_name": "email",
    "data_type": "email",
    "sample_value": "invalid-email",
    "constraints": "Must be valid email format",
    "test_category": "invalid"
  }}
]

Include at least 10-15 diverse test data sets covering all fields, formats, and edge cases.
"""

    def _parse_response(self, response_text: str) -> list[TestData]:
        """Extract JSON from response and convert to TestData objects."""
        try:
            # Try to find JSON array in the response
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1

            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON array found in response")

            json_str = response_text[start_idx:end_idx]
            test_data_list = json.loads(json_str)

            test_data = [TestData(**td) for td in test_data_list]
            return test_data
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error parsing response: {e}")
            return []
