# VQA Module

**Owner:** Person 1 (Abby)  
**Status:** To be implemented

## Purpose

The Visual Question Answering (VQA) module analyzes images and answers natural language questions about visual content such as objects, colors, scenes, and activities.

## Requirements

This module should implement the `answer_question()` function that will be called by the integration layer.

## Interface

```python
def answer_question(image_path: str, question: str) -> str:
    """
    Answer a visual question about an image.
    
    Args:
        image_path (str): Path to the image file
        question (str): The question to answer about the image
        
    Returns:
        str: The answer to the question
    """
    # Your implementation here
    pass
```

## Suggested Implementation

### Recommended Models
- **BLIP-2** (Salesforce)
- **LLaVA** (Large Language and Vision Assistant)
- **ViLT** (Vision-and-Language Transformer)

### Example with BLIP-2

```python
from transformers import BlipProcessor, BlipForQuestionAnswering
from PIL import Image

# Load model and processor (do this once, not per request)
processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")

def answer_question(image_path: str, question: str) -> str:
    # Load image
    image = Image.open(image_path).convert('RGB')
    
    # Process inputs
    inputs = processor(image, question, return_tensors="pt")
    
    # Generate answer
    outputs = model.generate(**inputs)
    answer = processor.decode(outputs[0], skip_special_tokens=True)
    
    return answer
```

## Setup Instructions

1. Install dependencies:
```bash
pip install torch transformers pillow
```

2. Implement the function in `vqa/vqa_model.py`

3. Test independently:
```bash
python vqa/vqa_model.py
```

## Example Usage

```python
from vqa.vqa_model import answer_question

# Test questions
answer = answer_question("car.jpg", "What color is the car?")
print(answer)  # Expected: "red" or "The car is red"

answer = answer_question("park.jpg", "How many people are there?")
print(answer)  # Expected: "3 people" or similar
```

## Test Cases

Create test examples in this directory with:
- Sample images
- Questions
- Expected answers
- Actual results

## Integration

Your module will be automatically called by the UI when:
- Questions are about visual content (colors, objects, scenes)
- Questions contain keywords like: "what color", "how many", "what is", "describe"

No changes needed to integration code - just implement the function!

## Dependencies to Add

Add to `requirements.txt`:
```
torch>=2.1.0
transformers>=4.35.0
```

## Resources

- [BLIP-2 Paper](https://arxiv.org/abs/2301.12597)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [VQA Dataset](https://visualqa.org/)
