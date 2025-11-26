<<<<<<< Updated upstream
=======
# VQA Module

**Owner:** Person 1 (Abby)  
**Status:** Implemented with BLIP-2-opt-2.7b

## Purpose

The Visual Question Answering (VQA) module analyzes images and answers natural language questions about visual content such as objects, colors, scenes, and activities using the BLIP-2-opt-2.7b model.

## Implementation Details

This module implements the `answer_question()` function that accepts an image path and a natural language question, then returns a detailed answer based on the image content using the BLIP-2-opt-2.7b vision-language model.

### Model: BLIP-2-opt-2.7b

- **Model ID:** `Salesforce/blip2-opt-2.7b`
- **Type:** Vision-Language Model (combines BLIP vision encoder with OPT 2.7B language model)
- **Size:** 2.7 billion parameters (lightweight, optimized for resource-constrained devices)
- **Capabilities:**
  - Image understanding and analysis
  - Natural language question answering about images
  - Visual descriptions
  - Object recognition and scene understanding

## Setup Instructions

### Prerequisites
- Python 3.8+
- CUDA 11.8+ (for GPU acceleration, optional but recommended)
- At least 6GB RAM (4GB minimum for CPU inference)

### Installation

1. **Install required packages:**
   ```bash
   pip install -r ../requirements.txt
   ```

2. **First run will download the model** (approximately 4-6GB):
   - The model will be automatically downloaded from Hugging Face on first use
   - Set the `HF_HOME` environment variable if you want to cache models elsewhere:
     ```bash
     export HF_HOME=/path/to/models
     ```

### GPU Setup (Recommended)

For optimal performance, use GPU acceleration:

```bash
# Verify CUDA is available
python -c "import torch; print(torch.cuda.is_available())"

# Monitor GPU usage during inference
nvidia-smi
```

## Usage

### Basic Usage

```python
from vqa.vqa_model import answer_question

# Answer a question about an image
answer = answer_question("path/to/image.jpg", "What color is the car?")
print(answer)
```

### Advanced Usage

```python
from vqa.vqa_model import load_model, answer_question, unload_model

# Manually load model for batch processing
model, processor, device = load_model()

# Process multiple images
images_and_questions = [
    ("image1.jpg", "What is in the image?"),
    ("image2.jpg", "How many people are there?"),
]

for image_path, question in images_and_questions:
    answer = answer_question(image_path, question)
    print(f"Q: {question}")
    print(f"A: {answer}\n")

# Clean up when done
unload_model()
```

### Flask Integration

The module is automatically integrated with the Flask backend. Simply upload an image and ask a question through the `/api/query` endpoint:

```bash
curl -X POST http://localhost:5001/api/query \
  -F "image=@test_image.jpg" \
  -F "question=What is in this image?"
```

## Performance Notes

### Device Selection
- **CUDA GPU:** Fastest inference (~1-2 seconds per question)
- **Apple MPS:** Medium speed (Mac with M1/M2 chips)
- **CPU:** Slower but functional (~10-15 seconds per question)

### Memory Usage
- **VRAM:** ~16GB for float16 inference on CUDA
- **RAM:** ~8GB for CPU inference
- Model is loaded once and reused for multiple queries

### Optimization Tips
1. Use GPU when possible for 5-10x speedup
2. Batch multiple questions together if processing large datasets
3. Adjust temperature and top_p parameters for different response styles:
   - Lower temperature (0.3-0.5): More conservative, consistent answers
   - Higher temperature (0.9-1.0): More creative, varied answers

## Function Reference

### `answer_question(image_path: str, question: str) -> str`
Main function to answer a visual question about an image.

**Parameters:**
- `image_path` (str): Path to the image file (supports PNG, JPG, GIF, WebP)
- `question` (str): Natural language question about the image

**Returns:**
- `str`: Answer to the question

**Raises:**
- `FileNotFoundError`: If image file doesn't exist
- `ValueError`: If question is empty or invalid
- `Exception`: If model inference fails

### `load_model() -> tuple`
Explicitly load the model and processor (cached, only loads once).

**Returns:**
- `tuple`: (model, processor, device)

### `unload_model() -> None`
Unload the model and free GPU memory.

## Testing

```bash
# Test with command line
python vqa/vqa_model.py path/to/image.jpg "Your question here"

# Example
python vqa/vqa_model.py ../data/samples/test_image.jpg "What is in this image?"
```

## Model Information

- **Source:** https://huggingface.co/llava-hf/llava-1.5-7b-hf
- **Architecture:** Vision-Language Transformer
- **Vision Encoder:** CLIP ViT-L/14
- **Language Model:** Llama-2-7B
- **Training Data:** LLaVA-Instruct-80K dataset
- **License:** Apache 2.0

## Troubleshooting

### Out of Memory (OOM) Error
- Reduce batch size or switch to CPU inference
- Ensure no other GPU processes are running
- Clear GPU cache with `torch.cuda.empty_cache()`

### Model Download Fails
- Check internet connection
- Ensure sufficient disk space (~20GB)
- Set HF token if required: `huggingface-cli login`

### Slow Inference
- Verify GPU is being used: `torch.cuda.is_available()`
- Check if CUDA is properly installed
- Profile with: `torch.profiler`

## References

- LLaVA Paper: https://arxiv.org/abs/2304.08485
- Hugging Face Model: https://huggingface.co/llava-hf/llava-1.5-7b-hf
- CLIP Paper: https://arxiv.org/abs/2103.14030
- Llama 2 Paper: https://arxiv.org/abs/2307.09288

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
>>>>>>> Stashed changes
