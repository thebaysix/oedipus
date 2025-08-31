# Sample Test Datasets

This directory contains sample datasets for testing the Oedipus React Frontend comparative analysis functionality.

## Files

### `sample_inputs.csv`
- **100 input records** with `input_id` and `input_text` columns
- 1:1 mapping of input_id to input_text
- Diverse topics: science, technology, nature, AI, physics, etc.
- Suitable for testing data upload, validation, and preview functionality

### `sample_outputs_model_a.csv` 
- **100 output records** from "Model A"
- Format: `input_id`, `output_text`
- Some input_ids have multiple completions (1:many relationship)
- Academic/technical writing style
- Detailed, comprehensive responses

### `sample_outputs_model_b.csv`
- **56 output records** from "Model B" 
- Format: `input_id`, `output_text`
- Conversational, engaging writing style
- Uses analogies and simplified explanations
- Some overlap with Model A prompts for comparison testing

## Usage Instructions

### 1. Test Single Dataset Upload
```
1. Navigate to React app: http://localhost:3000
2. Upload sample_inputs.csv
3. Verify data preview shows 100 prompts
4. Upload sample_outputs_model_a.csv
5. Create single analysis
```

### 2. Test Comparative Analysis
```
1. Upload sample_inputs.csv
2. Upload sample_outputs_model_a.csv (label as "Technical Model")
3. Upload sample_outputs_model_b.csv (label as "Conversational Model")
4. Create comparison analysis
5. Review side-by-side results, charts, and insights
```

### 3. Test Edge Cases
```
- Upload prompts without completions
- Upload completions without matching prompts
- Test CSV validation errors
- Test large dataset handling
```

## Expected Analysis Results

### Model A (Technical)
- **Style**: Academic, detailed, comprehensive
- **Length**: Generally longer responses
- **Tone**: Professional, informative
- **Structure**: Well-organized, systematic

### Model B (Conversational)
- **Style**: Engaging, analogical, simplified
- **Length**: Variable, often with examples
- **Tone**: Friendly, accessible
- **Structure**: Narrative, example-driven

### Comparison Metrics
The analysis should reveal:
- **Response Length Differences**: Model A typically longer
- **Vocabulary Complexity**: Model A more technical terms
- **Engagement Style**: Model B more analogies and questions
- **Coverage**: Model A covers more input_ids
- **Consistency**: Different approaches to same questions

## Data Characteristics

### Input Distribution
- Science & Technology: 40%
- Physics & Chemistry: 25%
- Biology & Medicine: 20%
- Computing & AI: 15%

### Output Patterns
- **Model A**: Covers input_ids 1-50 (2 responses each)
- **Model B**: Covers input_ids 1-50 + additional responses for 25,30,35,40,45,50
- **Overlapping prompts**: 1-50 (perfect for comparison)
- **Model A only**: None
- **Model B only**: 6 additional responses

This structure allows testing both aligned comparisons (same prompts) and coverage analysis (different input coverage).