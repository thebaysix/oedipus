import numpy as np
from collections import Counter, defaultdict
from typing import List, Dict, Any


def calculate_empowerment(prompts: Dict[str, str], completions: Dict[str, List[str]]) -> float:
    """
    Calculate empowerment metric - influence of model decisions on output diversity.
    E = I(A;X'|X) = H(A|X) - H(A|X,X')
    
    Simplified version: measures how much the model's choice of output affects
    the diversity of possible next completions.
    """
    if not prompts or not completions:
        return 0.0
    
    # Group completions by prompt
    input_output_groups = defaultdict(list)
    for input_id, input_text in prompts.items():
        if input_id in completions:
            input_output_groups[input_text].extend(completions[input_id])
    
    if not input_output_groups:
        return 0.0
    
    total_empowerment = 0.0
    total_weight = 0.0
    
    # Calculate empowerment for each prompt group
    for input_text, output_list in input_output_groups.items():
        if len(output_list) < 2:
            continue
        
        # Calculate diversity of completions for this prompt
        output_counts = Counter(output_list)
        group_size = len(output_list)
        
        # Calculate entropy of output distribution for this prompt
        output_entropy = 0.0
        for count in output_counts.values():
            p = count / group_size
            if p > 0:
                output_entropy -= p * np.log2(p)
        
        # Weight by frequency of this prompt
        weight = group_size
        total_empowerment += weight * output_entropy
        total_weight += weight
    
    return total_empowerment / total_weight if total_weight > 0 else 0.0


def calculate_output_diversity_metrics(prompts: Dict[str, str], completions: Dict[str, List[str]]) -> Dict[str, float]:
    """
    Calculate various output diversity metrics.
    """
    if not prompts or not completions:
        return {
            "empowerment": 0.0,
            "average_outputs_per_input": 0.0,
            "unique_outputs_ratio": 0.0,
            "output_length_variance": 0.0
        }
    
    empowerment = calculate_empowerment(prompts, completions)
    
    # Calculate average number of completions per prompt
    output_counts = [len(completions.get(input_id, [])) for input_id in prompts.keys()]
    avg_outputs = np.mean(output_counts) if output_counts else 0.0
    
    # Calculate unique completions ratio
    all_outputs = []
    for input_id in prompts.keys():
        if input_id in completions:
            all_outputs.extend(completions[input_id])
    
    unique_ratio = len(set(all_outputs)) / len(all_outputs) if all_outputs else 0.0
    
    # Calculate output length variance
    output_lengths = [len(output) for output in all_outputs]
    length_variance = np.var(output_lengths) if output_lengths else 0.0
    
    return {
        "empowerment": empowerment,
        "average_outputs_per_input": avg_outputs,
        "unique_outputs_ratio": unique_ratio,
        "output_length_variance": float(length_variance)
    }