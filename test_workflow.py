"""
Test script to run the workflow locally without API.
Usage: python test_workflow.py
"""

import os
import json
from dotenv import load_dotenv
from orchestrator.workflow import Q360Workflow

# Load environment variables
load_dotenv()

# Initialize workflow
workflow = Q360Workflow(
    gemini_api_key=os.getenv("GEMINI_API_KEY"),
    jira_url=os.getenv("JIRA_URL"),
    jira_email=os.getenv("JIRA_EMAIL"),
    jira_api_token=os.getenv("JIRA_API_TOKEN"),
)


def test_workflow(jira_issue_key: str):
    """Test the complete workflow."""
    print(f"\n{'='*60}")
    print(f"Testing Q360 Workflow for: {jira_issue_key}")
    print("=" * 60)

    result = workflow.execute(jira_issue_key)

    if result.get("error"):
        print(f"❌ Error: {result['error']}")
        return

    print(f"\n✅ Story Summary: {result.get('story_summary')}")

    # Print test cases
    test_cases = result.get("test_cases", [])
    print(f"\n📋 Generated {len(test_cases)} Test Cases:")
    print("-" * 60)
    for tc in test_cases:
        print(f"ID: {tc['test_id']}")
        print(f"Title: {tc['title']}")
        print(f"Type: {tc['test_type']} | Priority: {tc['priority']}")
        print(f"Steps: {len(tc['steps'])} steps")
        print(f"Expected: {tc['expected_result']}")
        print("-" * 60)

    # Print test data
    test_data = result.get("test_data", [])
    print(f"\n📊 Generated {len(test_data)} Test Data Points:")
    print("-" * 60)

    # Group by field name
    fields = {}
    for td in test_data:
        field = td["field_name"]
        if field not in fields:
            fields[field] = []
        fields[field].append(td)

    for field_name, data_points in fields.items():
        print(f"\nField: {field_name}")
        for dp in data_points:
            print(
                f"  - [{dp['test_category']}] {dp['sample_value']} ({dp['data_type']})"
            )
            print(f"    Constraints: {dp['constraints']}")

    # Save results to file
    output_file = f"results_{jira_issue_key}.json"
    with open(output_file, "w") as f:
        json.dump(result, f, indent=2)

    print(f"\n✅ Results saved to: {output_file}")


if __name__ == "__main__":
    # Test with a Jira issue key
    # Replace with your actual Jira issue key
    jira_issue = input("Enter Jira issue key (e.g., PROJ-123): ").strip()

    if not jira_issue:
        print("❌ Issue key required. Example: PROJ-123")
    else:
        try:
            test_workflow(jira_issue)
        except Exception as e:
            print(f"❌ Error running workflow: {e}")
            import traceback

            traceback.print_exc()
