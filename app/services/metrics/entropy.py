import numpy as np
from collections import Counter
from typing import List, Dict, Any


def calculate_input_entropy(prompts: Dict[str, str]) -> float:
    """
    Calculate entropy of input distribution.
    H(X) = -Σ p(x) log p(x)
    """
    if not prompts:
        return 0.0
    
    # Count frequency of each unique input
    input_counts = Counter(prompts.values())
    total_inputs = len(prompts)
    
    # Calculate probabilities and entropy
    entropy = 0.0
    for count in input_counts.values():
        p = count / total_inputs
        if p > 0:
            entropy -= p * np.log2(p)
    
    return entropy


def calculate_response_entropy(prompts: Dict[str, str], completions: Dict[str, List[str]]) -> float:
    """
    Calculate conditional entropy of completions given prompts.
    H(Y|X) = -Σ p(x,y) log p(y|x)
    """
    if not prompts or not completions:
        return 0.0
    
    total_pairs = 0
    conditional_entropy = 0.0
    
    # Group by input value
    input_groups = {}
    for input_id, input_text in prompts.items():
        if input_text not in input_groups:
            input_groups[input_text] = []
        if input_id in completions:
            input_groups[input_text].extend(completions[input_id])
    
    # Calculate conditional entropy for each input group
    for input_text, output_list in input_groups.items():
        if not output_list:
            continue
            
        # Count output frequencies for this input
        output_counts = Counter(output_list)
        group_total = len(output_list)
        total_pairs += group_total
        
        # Calculate entropy for this input group
        group_entropy = 0.0
        for count in output_counts.values():
            p_y_given_x = count / group_total
            if p_y_given_x > 0:
                group_entropy -= p_y_given_x * np.log2(p_y_given_x)
        
        # Weight by probability of this input
        p_x = group_total / sum(len(ol) for ol in input_groups.values())
        conditional_entropy += p_x * group_entropy
    
    return conditional_entropy