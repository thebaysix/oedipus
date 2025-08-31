#!/usr/bin/env python3
"""
Test script to verify the comparison analysis fix.
"""
import requests
import json
import time
import uuid

BASE_URL = "http://localhost:8000"

def create_test_dataset():
    """Create a test prompt dataset."""
    dataset_data = {
        "name": f"Test Prompts {uuid.uuid4().hex[:8]}",
        "prompts": {
            "prompt_1": "What is the capital of France?",
            "prompt_2": "Explain machine learning in simple terms.",
            "prompt_3": "Write a short story about a robot."
        },
        "metadata": {"test": True}
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/datasets/", json=dataset_data)
    if response.status_code == 201:
        print(f"✓ Created prompt dataset: {response.json()['id']}")
        return response.json()
    else:
        print(f"✗ Failed to create prompt dataset: {response.status_code} - {response.text}")
        return None

def create_test_completion_dataset(dataset_id, name_suffix):
    """Create a test completion dataset."""
    completion_data = {
        "name": f"Test Completions {name_suffix}",
        "dataset_id": dataset_id,
        "completions": {
            "prompt_1": ["Paris is the capital of France.", "The capital of France is Paris."],
            "prompt_2": ["Machine learning is AI that learns from data.", "ML uses algorithms to find patterns in data."],
            "prompt_3": ["Once upon a time, there was a helpful robot named Bob.", "A robot named Alice helped people every day."]
        },
        "metadata": {"test": True, "model": name_suffix}
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/datasets/{dataset_id}/completions", json=completion_data)
    if response.status_code == 201:
        print(f"✓ Created completion dataset: {response.json()['id']}")
        return response.json()
    else:
        print(f"✗ Failed to create completion dataset: {response.status_code} - {response.text}")
        return None

def create_test_comparison(dataset_id, completion_ids):
    """Create a test comparison."""
    comparison_data = {
        "name": f"Test Comparison {uuid.uuid4().hex[:8]}",
        "dataset_id": dataset_id,
        "completion_dataset_ids": completion_ids,
        "alignment_key": "prompt_id"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/comparisons/create", json=comparison_data)
    if response.status_code == 201:
        result = response.json()
        print(f"✓ Created comparison: {result['id']}")
        print(f"  Status: {result['status']}")
        return result
    else:
        print(f"✗ Failed to create comparison: {response.status_code} - {response.text}")
        return None

def check_comparison_status(comparison_id):
    """Check the status of a comparison."""
    response = requests.get(f"{BASE_URL}/api/v1/comparisons/{comparison_id}")
    if response.status_code == 200:
        result = response.json()
        print(f"  Comparison {comparison_id}: {result['status']}")
        if result['status'] == 'completed':
            print(f"  ✓ Analysis completed successfully!")
            print(f"  Metrics: {len(result.get('statistical_results', {}).get('metrics', []))}")
            print(f"  Insights: {len(result.get('automated_insights', []))}")
            return True
        elif result['status'] == 'failed':
            print(f"  ✗ Analysis failed: {result.get('statistical_results', {}).get('error', 'Unknown error')}")
            return False
        return None  # Still running
    else:
        print(f"✗ Failed to check comparison: {response.status_code}")
        return False

def main():
    print("🧪 Testing Comparison Analysis Fix")
    print("=" * 50)
    
    # Create test data
    print("\n1. Creating test datasets...")
    dataset = create_test_dataset()
    if not dataset:
        return
    
    completion1 = create_test_completion_dataset(dataset['id'], "Model_A")
    completion2 = create_test_completion_dataset(dataset['id'], "Model_B")
    
    if not completion1 or not completion2:
        return
    
    # Create comparison
    print("\n2. Creating comparison...")
    comparison = create_test_comparison(dataset['id'], [completion1['id'], completion2['id']])
    if not comparison:
        return
    
    # Monitor progress
    print("\n3. Monitoring analysis progress...")
    max_attempts = 30  # 30 seconds max
    for attempt in range(max_attempts):
        result = check_comparison_status(comparison['id'])
        if result is True:
            print("\n🎉 SUCCESS: Analysis completed!")
            break
        elif result is False:
            print("\n💥 FAILED: Analysis failed!")
            break
        else:
            time.sleep(1)
    else:
        print(f"\n⏰ TIMEOUT: Analysis did not complete within {max_attempts} seconds")
    
    print("\n" + "=" * 50)
    print("Test completed.")

if __name__ == "__main__":
    main()