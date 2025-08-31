"""
Statistical tests for comparing completion datasets.
"""
import numpy as np
from typing import Dict, List, Any
from scipy import stats
import math


def run_statistical_tests(completions_by_dataset: Dict[str, Dict[str, List[str]]]) -> List[Dict[str, Any]]:
    """
    Run statistical tests comparing multiple completion datasets.
    
    Args:
        completions_by_dataset: Dict mapping dataset_name -> {prompt_id -> [completions]}
    
    Returns:
        List of statistical metrics comparing datasets
    """
    dataset_names = list(completions_by_dataset.keys())
    if len(dataset_names) < 2:
        return []
    
    metrics = []
    
    # Compare each pair of datasets
    for i in range(len(dataset_names)):
        for j in range(i + 1, len(dataset_names)):
            dataset_a = dataset_names[i]
            dataset_b = dataset_names[j]
            
            # Get metrics for both datasets
            metrics_a = _calculate_dataset_metrics(completions_by_dataset[dataset_a])
            metrics_b = _calculate_dataset_metrics(completions_by_dataset[dataset_b])
            
            # Run statistical tests for each metric
            for metric_name in metrics_a.keys():
                if metric_name in metrics_b:
                    values_a = metrics_a[metric_name]
                    values_b = metrics_b[metric_name]
                    
                    if len(values_a) > 1 and len(values_b) > 1:
                        stat_result = _run_t_test(values_a, values_b)
                        
                        metrics.append({
                            "name": f"{metric_name} ({dataset_a} vs {dataset_b})",
                            "dataset_a": dataset_a,
                            "dataset_b": dataset_b,
                            "dataset_a_value": np.mean(values_a),
                            "dataset_b_value": np.mean(values_b),
                            "statistical_significance": stat_result["p_value"],
                            "effect_size": stat_result["effect_size"],
                            "confidence_interval_lower": stat_result["ci_lower"],
                            "confidence_interval_upper": stat_result["ci_upper"],
                            "test_statistic": stat_result["statistic"],
                            "degrees_of_freedom": stat_result["df"]
                        })
    
    return metrics


def _calculate_dataset_metrics(completions: Dict[str, List[str]]) -> Dict[str, List[float]]:
    """Calculate various metrics for a single completion dataset."""
    metrics = {
        "completion_length": [],
        "completion_count": [],
        "unique_completions": [],
        "avg_word_count": [],
        "response_diversity": []
    }
    
    for prompt_id, completion_list in completions.items():
        if not completion_list:
            continue
            
        # Completion length (characters)
        lengths = [len(comp) for comp in completion_list]
        metrics["completion_length"].extend(lengths)
        
        # Completion count per prompt
        metrics["completion_count"].append(len(completion_list))
        
        # Unique completions per prompt
        unique_count = len(set(completion_list))
        metrics["unique_completions"].append(unique_count)
        
        # Average word count
        word_counts = [len(comp.split()) for comp in completion_list]
        metrics["avg_word_count"].extend(word_counts)
        
        # Response diversity (ratio of unique to total)
        diversity = unique_count / len(completion_list) if completion_list else 0
        metrics["response_diversity"].append(diversity)
    
    return metrics


def _run_t_test(values_a: List[float], values_b: List[float]) -> Dict[str, float]:
    """Run independent t-test between two groups of values."""
    try:
        # Convert to numpy arrays
        a = np.array(values_a)
        b = np.array(values_b)
        
        # Remove any NaN or infinite values
        a = a[np.isfinite(a)]
        b = b[np.isfinite(b)]
        
        if len(a) < 2 or len(b) < 2:
            return {
                "statistic": 0.0,
                "p_value": 1.0,
                "effect_size": 0.0,
                "ci_lower": 0.0,
                "ci_upper": 0.0,
                "df": 0
            }
        
        # Run independent t-test
        statistic, p_value = stats.ttest_ind(a, b, equal_var=False)  # Welch's t-test
        
        # Calculate effect size (Cohen's d)
        pooled_std = np.sqrt(((len(a) - 1) * np.var(a, ddof=1) + (len(b) - 1) * np.var(b, ddof=1)) / (len(a) + len(b) - 2))
        effect_size = (np.mean(a) - np.mean(b)) / pooled_std if pooled_std > 0 else 0.0
        
        # Calculate confidence interval for the difference in means
        se_diff = np.sqrt(np.var(a, ddof=1) / len(a) + np.var(b, ddof=1) / len(b))
        df = len(a) + len(b) - 2
        t_critical = stats.t.ppf(0.975, df)  # 95% confidence interval
        mean_diff = np.mean(a) - np.mean(b)
        ci_lower = mean_diff - t_critical * se_diff
        ci_upper = mean_diff + t_critical * se_diff
        
        return {
            "statistic": float(statistic) if not np.isnan(statistic) else 0.0,
            "p_value": float(p_value) if not np.isnan(p_value) else 1.0,
            "effect_size": float(effect_size) if not np.isnan(effect_size) else 0.0,
            "ci_lower": float(ci_lower) if not np.isnan(ci_lower) else 0.0,
            "ci_upper": float(ci_upper) if not np.isnan(ci_upper) else 0.0,
            "df": int(df)
        }
        
    except Exception as e:
        # Return safe defaults if calculation fails
        return {
            "statistic": 0.0,
            "p_value": 1.0,
            "effect_size": 0.0,
            "ci_lower": 0.0,
            "ci_upper": 0.0,
            "df": 0
        }


def calculate_summary_statistics(completions_by_dataset: Dict[str, Dict[str, List[str]]]) -> Dict[str, Any]:
    """Calculate summary statistics for all datasets."""
    summary = {}
    
    for dataset_name, completions in completions_by_dataset.items():
        metrics = _calculate_dataset_metrics(completions)
        
        dataset_summary = {}
        for metric_name, values in metrics.items():
            if values:
                dataset_summary[metric_name] = {
                    "mean": float(np.mean(values)),
                    "std": float(np.std(values)),
                    "min": float(np.min(values)),
                    "max": float(np.max(values)),
                    "count": len(values)
                }
            else:
                dataset_summary[metric_name] = {
                    "mean": 0.0,
                    "std": 0.0,
                    "min": 0.0,
                    "max": 0.0,
                    "count": 0
                }
        
        summary[dataset_name] = dataset_summary
    
    return summary