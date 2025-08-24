import numpy as np
import tiktoken
from typing import List, Dict, Any
from collections import Counter


def calculate_character_metrics(outputs: Dict[str, List[str]]) -> Dict[str, Any]:
    """Calculate character-based metrics for outputs."""
    all_outputs = []
    for output_list in outputs.values():
        all_outputs.extend(output_list)
    
    if not all_outputs:
        return {
            "character_count_mean": 0.0,
            "character_count_std": 0.0,
            "character_count_min": 0,
            "character_count_max": 0,
            "character_count_distribution": {}
        }
    
    char_counts = [len(output) for output in all_outputs]
    
    # Create distribution bins
    if char_counts:
        min_chars, max_chars = min(char_counts), max(char_counts)
        if max_chars > min_chars:
            bins = np.linspace(min_chars, max_chars, min(10, max_chars - min_chars + 1))
            hist, bin_edges = np.histogram(char_counts, bins=bins)
            distribution = {
                f"{int(bin_edges[i])}-{int(bin_edges[i+1])}": int(hist[i])
                for i in range(len(hist))
            }
        else:
            distribution = {str(min_chars): len(char_counts)}
    else:
        distribution = {}
    
    return {
        "character_count_mean": float(np.mean(char_counts)),
        "character_count_std": float(np.std(char_counts)),
        "character_count_min": int(min(char_counts)),
        "character_count_max": int(max(char_counts)),
        "character_count_distribution": distribution
    }


def calculate_token_metrics(outputs: Dict[str, List[str]]) -> Dict[str, Any]:
    """Calculate token-based metrics using tiktoken."""
    try:
        encoding = tiktoken.get_encoding("cl100k_base")  # GPT-4 encoding
    except Exception:
        # Fallback to simple word counting if tiktoken fails
        return calculate_word_metrics(outputs)
    
    all_outputs = []
    for output_list in outputs.values():
        all_outputs.extend(output_list)
    
    if not all_outputs:
        return {
            "token_count_mean": 0.0,
            "token_count_std": 0.0,
            "token_count_min": 0,
            "token_count_max": 0,
            "token_count_distribution": {}
        }
    
    token_counts = []
    for output in all_outputs:
        try:
            tokens = encoding.encode(output)
            token_counts.append(len(tokens))
        except Exception:
            # Fallback to word count
            token_counts.append(len(output.split()))
    
    # Create distribution bins
    if token_counts:
        min_tokens, max_tokens = min(token_counts), max(token_counts)
        if max_tokens > min_tokens:
            bins = np.linspace(min_tokens, max_tokens, min(10, max_tokens - min_tokens + 1))
            hist, bin_edges = np.histogram(token_counts, bins=bins)
            distribution = {
                f"{int(bin_edges[i])}-{int(bin_edges[i+1])}": int(hist[i])
                for i in range(len(hist))
            }
        else:
            distribution = {str(min_tokens): len(token_counts)}
    else:
        distribution = {}
    
    return {
        "token_count_mean": float(np.mean(token_counts)),
        "token_count_std": float(np.std(token_counts)),
        "token_count_min": int(min(token_counts)),
        "token_count_max": int(max(token_counts)),
        "token_count_distribution": distribution
    }


def calculate_word_metrics(outputs: Dict[str, List[str]]) -> Dict[str, Any]:
    """Calculate word-based metrics as fallback."""
    all_outputs = []
    for output_list in outputs.values():
        all_outputs.extend(output_list)
    
    if not all_outputs:
        return {
            "word_count_mean": 0.0,
            "word_count_std": 0.0,
            "word_count_min": 0,
            "word_count_max": 0,
            "word_count_distribution": {}
        }
    
    word_counts = [len(output.split()) for output in all_outputs]
    
    # Create distribution bins
    if word_counts:
        min_words, max_words = min(word_counts), max(word_counts)
        if max_words > min_words:
            bins = np.linspace(min_words, max_words, min(10, max_words - min_words + 1))
            hist, bin_edges = np.histogram(word_counts, bins=bins)
            distribution = {
                f"{int(bin_edges[i])}-{int(bin_edges[i+1])}": int(hist[i])
                for i in range(len(hist))
            }
        else:
            distribution = {str(min_words): len(word_counts)}
    else:
        distribution = {}
    
    return {
        "word_count_mean": float(np.mean(word_counts)),
        "word_count_std": float(np.std(word_counts)),
        "word_count_min": int(min(word_counts)),
        "word_count_max": int(max(word_counts)),
        "word_count_distribution": distribution
    }