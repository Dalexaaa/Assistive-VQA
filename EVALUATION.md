# Assistive-VQA System Evaluation

This directory contains evaluation scripts and results for the Assistive-VQA system.

## Quick Start

Run the comprehensive evaluation:

```bash
python evaluate_system.py
```

This will:
- Test VQA model accuracy
- Test OCR model accuracy  
- Test routing logic accuracy
- Measure response times
- Generate detailed metrics report

## Output

The script generates:
- **Console output**: Real-time test results and summary
- **evaluation_results.json**: Detailed results with timestamps

## Metrics Measured

### VQA Module
- Accuracy (% correct answers)
- Average response time
- Total tests passed/failed

### OCR Module
- Accuracy (% correct text extraction)
- Average response time
- Total tests passed/failed

### Routing Logic
- Accuracy (% correct module selection)
- Total routing decisions

### Overall System
- Combined accuracy across all modules
- Total system performance

## Test Cases

Test cases are defined in `data/cases.csv` with the following format:

```csv
image_path,question,expected_module,expected_output,notes
samples/stop_sign.jpg,What does the sign say?,ocr,STOP,Text recognition test
samples/red_car.jpg,What color is the car?,vqa,The car is red,Color identification test
```

## Adding Test Cases

To add new test cases, edit `data/cases.csv`:

1. Add image to appropriate location
2. Add row with: image_path, question, expected_module (vqa/ocr), expected_output, notes
3. Run evaluation script

## Evaluation Criteria

**Answer Matching:**
- Exact match (case-insensitive)
- Substring match (expected in actual)
- Word overlap (60% threshold)

**Routing Accuracy:**
- Correct module selected based on question keywords

**Response Time:**
- Measured from function call to return
- Averaged across all test cases
