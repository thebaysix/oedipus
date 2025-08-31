import json
import pandas as pd
from typing import Dict, Any, List, Tuple


def validate_input_json(json_data: str) -> Tuple[bool, str, Dict]:
    """
    Validate input JSON format.
    Expected format: {inputId: input_string}
    """
    try:
        data = json.loads(json_data)
        
        if not isinstance(data, dict):
            return False, "JSON must be a dictionary", {}
        
        # Check that all values are strings
        for key, value in data.items():
            if not isinstance(value, str):
                return False, f"All values must be strings. Found {type(value)} for key '{key}'", {}
        
        if len(data) == 0:
            return False, "JSON cannot be empty", {}
        
        return True, "Valid input format", data
        
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON format: {str(e)}", {}


def validate_output_json(json_data: str, input_keys: List[str]) -> Tuple[bool, str, Dict]:
    """
    Validate output JSON format.
    Expected format: {input_id: [output_string1, output_string2, ...]}
    """
    try:
        data = json.loads(json_data)
        
        if not isinstance(data, dict):
            return False, "JSON must be a dictionary", {}
        
        # Check format and validate against input keys
        input_key_set = set(input_keys)
        
        for key, value in data.items():
            if key not in input_key_set:
                return False, f"Output key '{key}' not found in prompt dataset", {}
            
            if not isinstance(value, list):
                return False, f"All values must be lists. Found {type(value)} for key '{key}'", {}
            
            # Check that all items in the list are strings
            for i, item in enumerate(value):
                if not isinstance(item, str):
                    return False, f"All output items must be strings. Found {type(item)} at index {i} for key '{key}'", {}
        
        if len(data) == 0:
            return False, "JSON cannot be empty", {}
        
        return True, "Valid output format", data
        
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON format: {str(e)}", {}


def format_metrics_for_display(results: Dict[str, Any]) -> Dict[str, Any]:
    """Format analysis results for better display in Streamlit."""
    formatted = {}
    
    # Information theory metrics
    if "information_theory" in results:
        it_metrics = results["information_theory"]
        formatted["Information Theory"] = {
            "Input Entropy": f"{it_metrics.get('input_entropy', 0):.4f}",
            "Response Entropy": f"{it_metrics.get('response_entropy', 0):.4f}",
            "Information Gain": f"{it_metrics.get('information_gain', 0):.4f}",
            "Normalized Information Gain": f"{it_metrics.get('normalized_information_gain', 0):.4f}"
        }
    
    # Diversity metrics
    if "diversity" in results:
        div_metrics = results["diversity"]
        formatted["Output Diversity"] = {
            "Empowerment": f"{div_metrics.get('empowerment', 0):.4f}",
            "Average Outputs per Input": f"{div_metrics.get('average_outputs_per_input', 0):.2f}",
            "Unique Outputs Ratio": f"{div_metrics.get('unique_outputs_ratio', 0):.4f}",
            "Output Length Variance": f"{div_metrics.get('output_length_variance', 0):.2f}"
        }
    
    # Character metrics
    if "character_metrics" in results:
        char_metrics = results["character_metrics"]
        formatted["Character Statistics"] = {
            "Mean Length": f"{char_metrics.get('character_count_mean', 0):.2f}",
            "Std Deviation": f"{char_metrics.get('character_count_std', 0):.2f}",
            "Min Length": char_metrics.get('character_count_min', 0),
            "Max Length": char_metrics.get('character_count_max', 0)
        }
    
    # Token metrics
    if "token_metrics" in results:
        token_metrics = results["token_metrics"]
        formatted["Token Statistics"] = {
            "Mean Tokens": f"{token_metrics.get('token_count_mean', 0):.2f}",
            "Std Deviation": f"{token_metrics.get('token_count_std', 0):.2f}",
            "Min Tokens": token_metrics.get('token_count_min', 0),
            "Max Tokens": token_metrics.get('token_count_max', 0)
        }
    
    # Summary
    if "summary" in results:
        summary = results["summary"]
        formatted["Summary"] = {
            "Total Inputs": summary.get('total_inputs', 0),
            "Total Outputs": summary.get('total_outputs', 0),
            "Unique Inputs": summary.get('unique_inputs', 0),
            "Unique Outputs": summary.get('unique_outputs', 0),
            "Avg Outputs per Input": f"{summary.get('avg_outputs_per_input', 0):.2f}",
            "Input Coverage": f"{summary.get('input_coverage', 0):.2%}"
        }
    
    return formatted


def create_sample_data() -> Tuple[Dict[str, str], Dict[str, List[str]]]:
    """Create sample data for demonstration."""
    sample_inputs = {
        "input_1": "What is the capital of France?",
        "input_2": "Explain quantum computing",
        "input_3": "Write a haiku about spring",
        "input_4": "What is 2+2?",
        "input_5": "Describe machine learning"
    }
    
    sample_outputs = {
        "input_1": [
            "The capital of France is Paris.",
            "Paris is the capital city of France.",
            "France's capital is Paris."
        ],
        "input_2": [
            "Quantum computing uses quantum mechanical phenomena to process information.",
            "It's a type of computation that harnesses quantum mechanics principles.",
            "Quantum computers use qubits instead of classical bits."
        ],
        "input_3": [
            "Cherry blossoms bloom\nGentle breeze carries petals\nSpring awakens life",
            "Flowers start to bloom\nWarm sunshine melts winter snow\nNature comes alive"
        ],
        "input_4": [
            "2+2 equals 4",
            "The answer is 4",
            "Four"
        ],
        "input_5": [
            "Machine learning is a subset of AI that enables computers to learn from data.",
            "It's a method of data analysis that automates analytical model building.",
            "ML algorithms build models based on training data to make predictions."
        ]
    }
    
    return sample_inputs, sample_outputs