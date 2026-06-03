"""
Direct test of Google Cloud Agents without Jira dependency.
Tests Google Cloud Agents API connectivity and agent functionality.
"""

import os
import json
from dotenv import load_dotenv
from agents.google_cloud_agent_factory import GoogleCloudAgentFactory

# Load environment variables
load_dotenv()

gcp_project_id = os.getenv("GCP_PROJECT_ID")
gcp_region = os.getenv("GCP_REGION", "us-central1")

if not gcp_project_id:
    print("[ERROR] GCP_PROJECT_ID not found in .env")
    exit(1)

print("=" * 60)
print("Testing Q360 Google Cloud Agents with Sample Story")
print("=" * 60)
print(f"\n[INFO] GCP Project: {gcp_project_id}")
print(f"[INFO] GCP Region: {gcp_region}\n")

# Sample story (no Jira needed)
sample_story = {
    "summary": "User registration with email validation",
    "description": "As a user, I want to register for a new account with my email and password",
    "acceptance_criteria": """
    - User should be able to enter email and password
    - Password must be at least 8 characters
    - Email must be valid format
    - User should receive confirmation email
    - Duplicate email registration should be rejected
    """
}

print(f"\n[STORY] {sample_story['summary']}\n")

# Test 1: Test Case Generator
print("[TEST 1] Testing Google Cloud Test Case Generator Agent...")
print("-" * 60)

try:
    agent_factory = GoogleCloudAgentFactory(gcp_project_id, gcp_region)
    tc_agent = agent_factory.create_test_case_generator_agent()
    test_cases = tc_agent.generate_test_cases(sample_story)

    print(f"[SUCCESS] Generated {len(test_cases)} test cases\n")

    for i, tc in enumerate(test_cases, 1):
        print(f"TC {i}: {tc.get('test_id', 'N/A')} - {tc.get('title', 'N/A')}")
        print(f"   Type: {tc.get('test_type', 'N/A')} | Priority: {tc.get('priority', 'N/A')}")
        print(f"   Steps: {len(tc.get('steps', []))}")
        print()

except Exception as e:
    print(f"[ERROR] Error in Test Case Generator: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 2: Test Data Generator
print("\n" + "=" * 60)
print("[TEST 2] Testing Google Cloud Test Data Generator Agent...")
print("-" * 60)

try:
    td_agent = agent_factory.create_test_data_generator_agent()
    test_data = td_agent.generate_test_data(test_cases, sample_story["summary"])

    print(f"[SUCCESS] Generated {len(test_data)} test data points\n")

    # Group by field
    fields = {}
    for td in test_data:
        field_name = td.get('field_name', 'unknown')
        if field_name not in fields:
            fields[field_name] = []
        fields[field_name].append(td)

    for field_name, data_points in fields.items():
        print(f"Field: {field_name}")
        for dp in data_points:
            print(f"  [{dp.get('test_category', 'N/A')}] {dp.get('sample_value', 'N/A')} ({dp.get('data_type', 'N/A')})")
        print()

except Exception as e:
    print(f"[ERROR] Error in Test Data Generator: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Summary
print("\n" + "=" * 60)
print("[SUCCESS] All agents working correctly!")
print("=" * 60)
print(f"\nResults:")
print(f"  - Test Cases Generated: {len(test_cases)}")
print(f"  - Test Data Generated: {len(test_data)}")
print(f"\n[INFO] Google Cloud Agents API is working perfectly!")

# Save results
output = {
    "story": sample_story,
    "test_cases": test_cases,
    "test_data": test_data
}

with open("test_results.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"\n[INFO] Results saved to: test_results.json")
