#!/usr/bin/env python3
"""
Test script to simulate the frontend flow and verify polling works correctly.
"""
import requests
import json
import time
import uuid

BASE_URL = "http://localhost:8000"

def create_test_data():
    """Create test data and return IDs."""
    # Create prompt dataset
    dataset_data = {
        "name": f"Frontend Test Prompts {uuid.uuid4().hex[:8]}",
        "prompts": {
            "prompt_1": "What is artificial intelligence?",
            "prompt_2": "Explain quantum computing.",
            "prompt_3": "Describe the future of technology."
        },
        "metadata": {"test": True}
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/datasets/", json=dataset_data)
    dataset = response.json()
    
    # Create completion datasets
    completion1_data = {
        "name": "GPT-4 Responses",
        "dataset_id": dataset['id'],
        "completions": {
            "prompt_1": ["AI is machine intelligence.", "Artificial intelligence simulates human cognition."],
            "prompt_2": ["Quantum computing uses quantum mechanics.", "It leverages quantum bits for computation."],
            "prompt_3": ["Technology will be more integrated.", "Future tech will be AI-driven and sustainable."]
        },
        "metadata": {"model": "gpt-4"}
    }
    
    completion2_data = {
        "name": "Claude Responses", 
        "dataset_id": dataset['id'],
        "completions": {
            "prompt_1": ["AI refers to computer systems that think.", "Machine intelligence that mimics humans."],
            "prompt_2": ["Quantum computers use quantum physics.", "They process information using quantum states."],
            "prompt_3": ["Technology will become more personalized.", "Future innovations will focus on sustainability."]
        },
        "metadata": {"model": "claude"}
    }
    
    comp1_response = requests.post(f"{BASE_URL}/api/v1/datasets/{dataset['id']}/completions", json=completion1_data)
    comp2_response = requests.post(f"{BASE_URL}/api/v1/datasets/{dataset['id']}/completions", json=completion2_data)
    
    return dataset['id'], comp1_response.json()['id'], comp2_response.json()['id']

def simulate_frontend_flow():
    """Simulate the complete frontend flow."""
    print("🎭 Simulating Frontend Flow")
    print("=" * 50)
    
    # Step 1: Create test data
    print("\n1. Creating test data...")
    dataset_id, comp1_id, comp2_id = create_test_data()
    print(f"✓ Created dataset: {dataset_id}")
    print(f"✓ Created completion 1: {comp1_id}")
    print(f"✓ Created completion 2: {comp2_id}")
    
    # Step 2: Create comparison (simulating frontend form submission)
    print("\n2. Creating comparison...")
    comparison_data = {
        "name": f"Frontend Test Comparison {uuid.uuid4().hex[:8]}",
        "dataset_id": dataset_id,
        "completion_dataset_ids": [comp1_id, comp2_id],
        "alignment_key": "prompt_id"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/comparisons/create", json=comparison_data)
    comparison = response.json()
    comparison_id = comparison['id']
    
    print(f"✓ Created comparison: {comparison_id}")
    print(f"  Initial status: {comparison['status']}")
    
    # Step 3: Simulate frontend polling (like useComparison hook)
    print("\n3. Simulating frontend polling...")
    poll_count = 0
    max_polls = 15  # 30 seconds max (2 second intervals)
    
    while poll_count < max_polls:
        poll_count += 1
        
        # Fetch comparison status (simulating React Query refetch)
        response = requests.get(f"{BASE_URL}/api/v1/comparisons/{comparison_id}")
        current_comparison = response.json()
        status = current_comparison['status']
        
        print(f"  Poll {poll_count}: Status = {status}")
        
        if status == 'completed':
            print("  ✅ Analysis completed!")
            
            # Check results
            metrics_count = len(current_comparison.get('statistical_results', {}).get('metrics', []))
            insights_count = len(current_comparison.get('automated_insights', []))
            alignment_count = len(current_comparison.get('statistical_results', {}).get('alignment', {}).get('alignedRows', []))
            
            print(f"  📊 Results:")
            print(f"    - Aligned rows: {alignment_count}")
            print(f"    - Statistical metrics: {metrics_count}")
            print(f"    - Automated insights: {insights_count}")
            
            # Show sample results
            if metrics_count > 0:
                sample_metric = current_comparison['statistical_results']['metrics'][0]
                print(f"  📈 Sample metric: {sample_metric['name']}")
                print(f"    - P-value: {sample_metric['statistical_significance']:.4f}")
                print(f"    - Effect size: {sample_metric['effect_size']:.4f}")
            
            if insights_count > 0:
                print(f"  💡 Sample insight: {current_comparison['automated_insights'][0]}")
            
            return True
            
        elif status == 'failed':
            print("  ❌ Analysis failed!")
            error = current_comparison.get('statistical_results', {}).get('error', 'Unknown error')
            print(f"  Error: {error}")
            return False
            
        elif status in ['pending', 'running']:
            print(f"  ⏳ Still {status}... (frontend would show progress bar)")
            time.sleep(2)  # Simulate 2-second polling interval
        else:
            print(f"  ❓ Unknown status: {status}")
            return False
    
    print(f"  ⏰ Timeout after {max_polls} polls")
    return False

def main():
    print("Testing complete frontend flow simulation...")
    
    try:
        success = simulate_frontend_flow()
        
        print("\n" + "=" * 50)
        if success:
            print("🎉 SUCCESS: Frontend flow simulation completed successfully!")
            print("✅ The polling mechanism works correctly")
            print("✅ Analysis completes and returns results")
            print("✅ Progress tracking would work as expected")
        else:
            print("💥 FAILED: Frontend flow simulation failed")
            print("❌ There may be issues with the polling or analysis")
        
    except Exception as e:
        print(f"\n💥 ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()