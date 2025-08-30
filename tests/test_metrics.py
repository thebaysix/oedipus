import pytest
from app.services.metrics.entropy import calculate_input_entropy, calculate_response_entropy
from app.services.metrics.information_gain import calculate_information_gain, calculate_mutual_information
from app.services.metrics.empowerment import calculate_empowerment, calculate_output_diversity_metrics
from app.services.metrics.basic_metrics import calculate_character_metrics, calculate_token_metrics

def test_input_entropy():
    """Test prompt entropy calculation."""
    prompts = {
        "input_1": "What is AI?",
        "input_2": "What is AI?",  # Duplicate
        "input_3": "What is ML?"
    }
    
    entropy = calculate_input_entropy(prompts)
    assert entropy > 0
    assert isinstance(entropy, float)

def test_response_entropy():
    """Test response entropy calculation."""
    prompts = {
        "input_1": "What is AI?",
        "input_2": "What is ML?"
    }
    
    completions = {
        "input_1": ["AI is artificial intelligence", "AI mimics human intelligence"],
        "input_2": ["ML is machine learning"]
    }
    
    entropy = calculate_response_entropy(prompts, completions)
    assert entropy >= 0
    assert isinstance(entropy, float)

def test_information_gain():
    """Test information gain calculation."""
    prompts = {
        "input_1": "What is AI?",
        "input_2": "What is ML?"
    }
    
    completions = {
        "input_1": ["AI is artificial intelligence"],
        "input_2": ["ML is machine learning"]
    }
    
    info_gain = calculate_information_gain(prompts, completions)
    assert info_gain >= 0
    assert isinstance(info_gain, float)

def test_mutual_information():
    """Test mutual information calculation."""
    prompts = {
        "input_1": "What is AI?",
        "input_2": "What is ML?",
        "input_3": "What is DL?"
    }
    
    completions = {
        "input_1": ["AI is artificial intelligence", "AI mimics human intelligence"],
        "input_2": ["ML is machine learning"],
        "input_3": ["DL is deep learning", "DL uses neural networks"]
    }
    
    mi_metrics = calculate_mutual_information(prompts, completions)
    
    assert "input_entropy" in mi_metrics
    assert "response_entropy" in mi_metrics
    assert "information_gain" in mi_metrics
    assert "normalized_information_gain" in mi_metrics
    
    for value in mi_metrics.values():
        assert isinstance(value, float)
        assert value >= 0

def test_empowerment():
    """Test empowerment calculation."""
    prompts = {
        "input_1": "What is AI?",
        "input_2": "What is ML?"
    }
    
    completions = {
        "input_1": ["Response 1", "Response 2", "Response 3"],
        "input_2": ["Response A"]
    }
    
    empowerment = calculate_empowerment(prompts, completions)
    assert empowerment >= 0
    assert isinstance(empowerment, float)

def test_output_diversity_metrics():
    """Test output diversity metrics."""
    prompts = {
        "input_1": "What is AI?",
        "input_2": "What is ML?",
        "input_3": "What is DL?"
    }
    
    completions = {
        "input_1": ["AI is artificial intelligence", "AI mimics human intelligence"],
        "input_2": ["ML is machine learning"],
        "input_3": ["DL is deep learning", "DL uses neural networks", "Deep learning is advanced ML"]
    }
    
    diversity_metrics = calculate_output_diversity_metrics(prompts, completions)
    
    expected_keys = [
        "empowerment",
        "average_outputs_per_input",
        "unique_outputs_ratio",
        "output_length_variance"
    ]
    
    for key in expected_keys:
        assert key in diversity_metrics
        assert isinstance(diversity_metrics[key], (int, float))
        assert diversity_metrics[key] >= 0

def test_character_metrics():
    """Test character metrics calculation."""
    completions = {
        "input_1": ["Short", "Medium length text"],
        "input_2": ["Very long text that has many characters in it"]
    }
    
    char_metrics = calculate_character_metrics(completions)
    
    expected_keys = [
        "character_count_mean",
        "character_count_std",
        "character_count_min",
        "character_count_max",
        "character_count_distribution"
    ]
    
    for key in expected_keys:
        assert key in char_metrics
    
    assert char_metrics["character_count_min"] <= char_metrics["character_count_max"]
    assert isinstance(char_metrics["character_count_distribution"], dict)

def test_token_metrics():
    """Test token metrics calculation."""
    completions = {
        "input_1": ["Hello world", "This is a longer sentence"],
        "input_2": ["Short"]
    }
    
    token_metrics = calculate_token_metrics(completions)
    
    # Should have either token metrics or word metrics (fallback)
    expected_keys = [
        "token_count_mean", "token_count_std", "token_count_min", 
        "token_count_max", "token_count_distribution"
    ]
    
    fallback_keys = [
        "word_count_mean", "word_count_std", "word_count_min",
        "word_count_max", "word_count_distribution"
    ]
    
    # Check if we have either token or word metrics
    has_token_metrics = all(key in token_metrics for key in expected_keys)
    has_word_metrics = all(key in token_metrics for key in fallback_keys)
    
    assert has_token_metrics or has_word_metrics

def test_empty_inputs():
    """Test metrics with empty prompts."""
    empty_inputs = {}
    empty_outputs = {}
    
    assert calculate_input_entropy(empty_inputs) == 0.0
    assert calculate_response_entropy(empty_inputs, empty_outputs) == 0.0
    assert calculate_information_gain(empty_inputs, empty_outputs) == 0.0
    assert calculate_empowerment(empty_inputs, empty_outputs) == 0.0