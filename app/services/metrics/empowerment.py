import numpy as np
from collections import Counter, defaultdict
from typing import List, Dict, Any


def calculate_empowerment(inputs: Dict[str, str], outputs: Dict[str, List[str]]) -> float:
    """
    Calculate empowerment metric - influence of model decisions on output diversity.
    E = I(A;X'|X) = H(A|X) - H(A|X,X')
    
    Simplified version: measures how much the model's choice of output affects
    the diversity of possible next outputs.
    """
    if not inputs or not outputs:
        return 0.0
    
    # Group outputs by input
    input_output_groups = defaultdict(list)
    for input_id, input_text in inputs.items():
        if input_id in outputs:
            input_output_groups[input_text].extend(outputs[input_id])
    
    if not input_output_groups:
        return 0.0
    
    total_empowerment = 0.0
    total_weight = 0.0
    
    # Calculate empowerment for each input group
    for input_text, output_list in input_output_groups.items():
        if len(output_list) < 2:
            continue
        
        # Calculate diversity of outputs for this input
        output_counts = Counter(output_list)
        group_size = len(output_list)
        
        # Calculate entropy of output distribution for this input
        output_entropy = 0.0
        for count in output_counts.values():
            p = count / group_size
            if p > 0:
                output_entropy -= p * np.log2(p)
        
        # Weight by frequency of this input
        weight = group_size
        total_empowerment += weight * output_entropy
        total_weight += weight
    
    return total_empowerment / total_weight if total_weight > 0 else 0.0


def calculate_output_diversity_metrics(inputs: Dict[str, str], outputs: Dict[str, List[str]]) -> Dict[str, float]:
    """
    Calculate various output diversity metrics.
    """
    if not inputs or not outputs:
        return {
            "empowerment": 0.0,
            "average_outputs_per_input": 0.0,
            "unique_outputs_ratio": 0.0,
            "output_length_variance": 0.0
        }
    
    empowerment = calculate_empowerment(inputs, outputs)
    
    # Calculate average number of outputs per input
    output_counts = [len(outputs.get(input_id, [])) for input_id in inputs.keys()]
    avg_outputs = np.mean(output_counts) if output_counts else 0.0
    
    # Calculate unique outputs ratio
    all_outputs = []
    for input_id in inputs.keys():
        if input_id in outputs:
            all_outputs.extend(outputs[input_id])
    
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