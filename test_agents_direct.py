"""
Direct test of agents without Jira dependency.
Tests Gemini API connectivity and agent functionality.
"""

import os
import json
from dotenv import load_dotenv
from agents.test_case_generator import TestCaseGeneratorAgent
from agents.test_data_generator import TestDataGeneratorAgent

# Load environment variables
load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")

if not gemini_key:
    print("❌ GEMINI_API_KEY not found in .env")
    exit(1)

print("=" * 60)
print("Testing Q360 Agents with Sample Story")
print("=" * 60)

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
print("[TEST 1] Testing Test Case Generator Agent...")
print("-" * 60)

try:
    tc_agent = TestCaseGeneratorAgent(gemini_key)
    test_cases = tc_agent.generate_test_cases(sample_story)

    print(f"[SUCCESS] Generated {len(test_cases)} test cases\n")

    for i, tc in enumerate(test_cases, 1):
        print(f"TC {i}: {tc.test_id} - {tc.title}")
        print(f"   Type: {tc.test_type} | Priority: {tc.priority}")
        print(f"   Steps: {len(tc.steps)}")
        print()

except Exception as e:
    print(f"[ERROR] Error in Test Case Generator: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 2: Test Data Generator
print("\n" + "=" * 60)
print("[TEST 2] Testing Test Data Generator Agent...")
print("-" * 60)

try:
    td_agent = TestDataGeneratorAgent(gemini_key)
    test_data = td_agent.generate_test_data(test_cases, sample_story["summary"])

    print(f"[SUCCESS] Generated {len(test_data)} test data points\n")

    # Group by field
    fields = {}
    for td in test_data:
        if td.field_name not in fields:
            fields[td.field_name] = []
        fields[td.field_name].append(td)

    for field_name, data_points in fields.items():
        print(f"Field: {field_name}")
        for dp in data_points:
            print(f"  [{dp.test_category}] {dp.sample_value} ({dp.data_type})")
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
print(f"\n[INFO] Gemini API is working perfectly!")

# Save results
output = {
    "story": sample_story,
    "test_cases": [tc.model_dump() for tc in test_cases],
    "test_data": [td.model_dump() for td in test_data]
}

with open("test_results.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"\n[INFO] Results saved to: test_results.json")
