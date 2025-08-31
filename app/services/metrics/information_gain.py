import numpy as np
from collections import Counter
from typing import List, Dict, Any
from .entropy import calculate_input_entropy, calculate_response_entropy


def calculate_information_gain(prompts: Dict[str, str], completions: Dict[str, List[str]]) -> float:
    """
    Calculate mutual information between prompts and completions.
    I(X;Y) = H(Y) - H(Y|X)
    """
    if not prompts or not completions:
        return 0.0
    
    # Calculate output entropy H(Y)
    all_outputs = []
    for input_id in prompts.keys():
        if input_id in completions:
            all_outputs.extend(completions[input_id])
    
    if not all_outputs:
        return 0.0
    
    output_counts = Counter(all_outputs)
    total_outputs = len(all_outputs)
    
    output_entropy = 0.0
    for count in output_counts.values():
        p = count / total_outputs
        if p > 0:
            output_entropy -= p * np.log2(p)
    
    # Calculate conditional entropy H(Y|X)
    conditional_entropy = calculate_response_entropy(prompts, completions)
    
    # Information gain = H(Y) - H(Y|X)
    return output_entropy - conditional_entropy


def calculate_mutual_information(prompts: Dict[str, str], completions: Dict[str, List[str]]) -> Dict[str, float]:
    """
    Calculate various mutual information metrics.
    """
    input_entropy = calculate_input_entropy(prompts)
    response_entropy = calculate_response_entropy(prompts, completions)
    information_gain = calculate_information_gain(prompts, completions)
    
    return {
        "input_entropy": input_entropy,
        "response_entropy": response_entropy,
        "information_gain": information_gain,
        "normalized_information_gain": information_gain / input_entropy if input_entropy > 0 else 0.0
    }