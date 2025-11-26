# VQA Module Testing Guide

## Unit Tests

Run the test suite:

```bash
cd ..
python -m pytest vqa/test_vqa.py -v
```

## Manual Testing

### 1. Test with Sample Image

```python
from vqa.vqa_model import answer_question

# Test with a sample image
image_path = "data/samples/image.jpg"
question = "What is the main object in this image?"
answer = answer_question(image_path, question)
print(f"Q: {question}")
print(f"A: {answer}")
```

### 2. Test Different Question Types

```python
from vqa.vqa_model import answer_question

image_path = "data/samples/image.jpg"

# Object detection
print(answer_question(image_path, "What objects are visible?"))

# Color identification
print(answer_question(image_path, "What colors are prominent?"))

# Activity recognition
print(answer_question(image_path, "What activity is happening?"))

# Scene understanding
print(answer_question(image_path, "Describe the scene in detail"))
```

### 3. Integration Testing

```bash
# Start the Flask backend
cd ui
python app.py

# Test via web interface at http://localhost:5000
# Upload an image and ask questions
```

## Performance Testing

### Timing Test
```python
import time
from vqa.vqa_model import answer_question

image_path = "data/samples/image.jpg"
question = "Describe this image in detail"

start = time.time()
answer = answer_question(image_path, question)
elapsed = time.time() - start

print(f"Response time: {elapsed:.2f}s")
print(f"Answer: {answer}")
```

### Memory Usage Test
```python
import psutil
import os
from vqa.vqa_model import load_model

process = psutil.Process(os.getpid())

# Check memory before loading
mem_before = process.memory_info().rss / 1024 / 1024
print(f"Memory before: {mem_before:.2f}MB")

# Load model
model, processor, device = load_model()

# Check memory after loading
mem_after = process.memory_info().rss / 1024 / 1024
print(f"Memory after: {mem_after:.2f}MB")
print(f"Model uses: {mem_after - mem_before:.2f}MB")
```

## Error Handling Testing

### Test Invalid Image
```python
from vqa.vqa_model import answer_question

try:
    answer = answer_question("nonexistent.jpg", "What's this?")
except FileNotFoundError as e:
    print(f"Correctly caught error: {e}")
```

### Test Empty Question
```python
from vqa.vqa_model import answer_question

try:
    answer = answer_question("data/samples/image.jpg", "")
except ValueError as e:
    print(f"Correctly caught error: {e}")
```

## Test Results Template

```
Test Date: YYYY-MM-DD
Model: LLaVA-1.5-7b-hf
Device: [CPU/GPU]
Python Version: 3.X.X

Test Results:
- Basic QA: ✓/✗
- Multiple Questions: ✓/✗
- Error Handling: ✓/✗
- Performance: {response_time}s
- Memory Usage: {memory_usage}MB

Notes:
```

## Continuous Testing

Run tests before committing:

```bash
# Run all tests
python -m pytest vqa/ -v

# Run specific test
python -m pytest vqa/test_vqa.py::test_answer_question -v

# Run with coverage
python -m pytest vqa/ --cov=vqa --cov-report=html
```
