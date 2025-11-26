# VQA Module Configuration

## Model Configuration

### Model Selection
- **Current Model:** BLIP-2-opt-2.7b
- **Model ID:** `Salesforce/blip2-opt-2.7b`
- **Type:** Vision-Language Model
- **Parameters:** 2.7 billion (lightweight)

### Environment Variables

```bash
# Hugging Face model cache directory
export HF_HOME=/path/to/models

# GPU device selection (if multiple GPUs)
export CUDA_VISIBLE_DEVICES=0

# Model precision (options: float32, float16, bfloat16)
export MODEL_PRECISION=float16
```

## Performance Tuning

### Memory Configuration

```python
# In vqa_model.py, adjust device_map:
model = LlavaForConditionalGeneration.from_pretrained(
    model_id,
    device_map="auto",  # Automatically split across available devices
    torch_dtype=torch.float16  # Use float16 for memory efficiency
)
```

### Inference Parameters

```python
# Generation settings
generation_config = {
    "max_new_tokens": 512,
    "temperature": 0.7,
    "top_p": 0.9,
}
```

## Model Details

### Input Specifications
- **Image Size:** Variable (model handles resizing)
- **Supported Formats:** JPEG, PNG, BMP, GIF
- **Color Space:** RGB

### Output Specifications
- **Answer Length:** Variable (up to max_new_tokens)
- **Answer Type:** Text description
- **Latency:** 5-30 seconds per image (depends on hardware)

## Troubleshooting

### Out of Memory Issues
1. Use `float16` precision (default)
2. Enable CPU offloading for layers
3. Use CPU-only mode for testing

### Slow Inference
1. Enable GPU acceleration
2. Pre-warm the model with dummy inputs
3. Use batch processing for multiple images

### Model Download Issues
1. Check internet connection
2. Ensure sufficient disk space (~20GB)
3. Manually download from Hugging Face Hub

## Advanced Configuration

### Custom Device Mapping
```python
device_map = {
    "vision_tower": 0,
    "multi_modal_projector": 0,
    "language_model": 0,
}
```

### Quantization (For Lower Memory Usage)
```python
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

model = LlavaForConditionalGeneration.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto"
)
```
