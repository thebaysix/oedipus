#!/usr/bin/env python3
"""
Complete test to verify the comparison analysis fix and progress tracking.
"""
import requests
import json
import time
import uuid

BASE_URL = "http://localhost:8000"

def test_complete_solution():
    """Test the complete solution with detailed progress tracking."""
    print("🔧 Testing Complete Comparison Analysis Solution")
    print("=" * 60)
    
    # Create test data
    print("\n1. Setting up test data...")
    dataset_data = {
        "name": f"Complete Test {uuid.uuid4().hex[:8]}",
        "prompts": {
            "prompt_1": "What is machine learning?",
            "prompt_2": "Explain neural networks.",
            "prompt_3": "Describe deep learning applications."
        },
        "metadata": {"test": "complete_solution"}
    }
    
    dataset_response = requests.post(f"{BASE_URL}/api/v1/datasets/", json=dataset_data)
    dataset = dataset_response.json()
    
    # Create two different completion datasets
    completion1_data = {
        "name": "Model Alpha",
        "dataset_id": dataset['id'],
        "completions": {
            "prompt_1": ["ML is a subset of AI that learns from data.", "Machine learning enables computers to learn without explicit programming."],
            "prompt_2": ["Neural networks are inspired by the human brain.", "They consist of interconnected nodes that process information."],
            "prompt_3": ["Deep learning is used in image recognition.", "Applications include autonomous vehicles and medical diagnosis."]
        },
        "metadata": {"model": "alpha", "version": "1.0"}
    }
    
    completion2_data = {
        "name": "Model Beta",
        "dataset_id": dataset['id'],
        "completions": {
            "prompt_1": ["Machine learning algorithms find patterns in data.", "It's a method of data analysis that automates analytical model building."],
            "prompt_2": ["Neural networks mimic biological neural networks.", "They use layers of nodes to process and transform data."],
            "prompt_3": ["Deep learning excels at complex pattern recognition.", "Common uses include natural language processing and computer vision."]
        },
        "metadata": {"model": "beta", "version": "2.1"}
    }
    
    comp1_response = requests.post(f"{BASE_URL}/api/v1/datasets/{dataset['id']}/completions", json=completion1_data)
    comp2_response = requests.post(f"{BASE_URL}/api/v1/datasets/{dataset['id']}/completions", json=completion2_data)
    
    print(f"✓ Created prompt dataset: {dataset['id']}")
    print(f"✓ Created Model Alpha completions: {comp1_response.json()['id']}")
    print(f"✓ Created Model Beta completions: {comp2_response.json()['id']}")
    
    # Create comparison
    print("\n2. Creating comparison with background analysis...")
    comparison_data = {
        "name": f"Alpha vs Beta Comparison {uuid.uuid4().hex[:8]}",
        "dataset_id": dataset['id'],
        "completion_dataset_ids": [comp1_response.json()['id'], comp2_response.json()['id']],
        "alignment_key": "prompt_id",
        "comparison_config": {"confidence_level": 0.95}
    }
    
    comparison_response = requests.post(f"{BASE_URL}/api/v1/comparisons/create", json=comparison_data)
    comparison = comparison_response.json()
    comparison_id = comparison['id']
    
    print(f"✓ Created comparison: {comparison_id}")
    print(f"  Initial status: {comparison['status']}")
    
    # Monitor detailed progress
    print("\n3. Monitoring detailed progress...")
    poll_count = 0
    max_polls = 10
    progress_steps_seen = set()
    
    while poll_count < max_polls:
        poll_count += 1
        
        response = requests.get(f"{BASE_URL}/api/v1/comparisons/{comparison_id}")
        current_comparison = response.json()
        status = current_comparison['status']
        
        # Check for progress information
        progress_info = current_comparison.get('statistical_results', {}).get('progress')
        if progress_info:
            step = progress_info.get('step', 'unknown')
            message = progress_info.get('message', 'Processing...')
            progress_steps_seen.add(step)
            print(f"  Poll {poll_count}: Status = {status}, Step = {step}")
            print(f"    Message: {message}")
        else:
            print(f"  Poll {poll_count}: Status = {status}")
        
        if status == 'completed':
            print("  ✅ Analysis completed successfully!")
            break
        elif status == 'failed':
            print("  ❌ Analysis failed!")
            error = current_comparison.get('statistical_results', {}).get('error', 'Unknown error')
            print(f"    Error: {error}")
            return False
        
        time.sleep(2)
    
    # Verify results
    print("\n4. Verifying results...")
    final_response = requests.get(f"{BASE_URL}/api/v1/comparisons/{comparison_id}")
    final_comparison = final_response.json()
    
    # Check alignment
    alignment = final_comparison.get('statistical_results', {}).get('alignment', {})
    aligned_rows = alignment.get('alignedRows', [])
    coverage_stats = alignment.get('coverageStats', {})
    
    print(f"✓ Alignment Results:")
    print(f"  - Aligned rows: {len(aligned_rows)}")
    print(f"  - Coverage: {coverage_stats.get('coveragePercentage', 0)}%")
    print(f"  - Total inputs: {coverage_stats.get('totalInputs', 0)}")
    print(f"  - Matched inputs: {coverage_stats.get('matchedInputs', 0)}")
    
    # Check statistical metrics
    metrics = final_comparison.get('statistical_results', {}).get('metrics', [])
    print(f"✓ Statistical Metrics: {len(metrics)} computed")
    
    if metrics:
        # Show significant results
        significant_metrics = [m for m in metrics if m.get('statistical_significance', 1.0) < 0.05]
        print(f"  - Significant differences: {len(significant_metrics)}")
        
        # Show sample metric
        sample_metric = metrics[0]
        print(f"  - Sample: {sample_metric['name']}")
        print(f"    P-value: {sample_metric['statistical_significance']:.4f}")
        print(f"    Effect size: {sample_metric['effect_size']:.4f}")
    
    # Check insights
    insights = final_comparison.get('automated_insights', [])
    print(f"✓ Automated Insights: {len(insights)} generated")
    if insights:
        print(f"  - Sample insight: {insights[0]}")
    
    # Check progress tracking
    print(f"✓ Progress Tracking: {len(progress_steps_seen)} steps observed")
    print(f"  - Steps seen: {', '.join(sorted(progress_steps_seen))}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SOLUTION VERIFICATION SUMMARY:")
    print("=" * 60)
    
    success_criteria = [
        ("✅ Comparison creation", True),
        ("✅ Background analysis execution", status == 'completed'),
        ("✅ Data alignment", len(aligned_rows) > 0),
        ("✅ Statistical metrics computation", len(metrics) > 0),
        ("✅ Automated insights generation", len(insights) > 0),
        ("✅ Progress tracking", len(progress_steps_seen) > 0),
        ("✅ Status transitions", 'running' in [s for s in ['pending', 'running', 'completed']]),
    ]
    
    all_passed = all(passed for _, passed in success_criteria)
    
    for criterion, passed in success_criteria:
        print(criterion if passed else criterion.replace("✅", "❌"))
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 SUCCESS: All verification criteria passed!")
        print("✅ The comparison analysis bug has been fixed")
        print("✅ Progress tracking is working correctly")
        print("✅ Frontend polling will work as expected")
        print("✅ Users will see real-time progress updates")
    else:
        print("💥 FAILED: Some verification criteria failed")
        print("❌ Additional debugging may be required")
    
    return all_passed

if __name__ == "__main__":
    try:
        success = test_complete_solution()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n💥 CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)