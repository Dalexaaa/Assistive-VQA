# VQA Module - Quick Start Guide

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Download the model (first time only):**
   ```bash
   python setup_vqa.py
   ```
   This downloads the BLIP-2-opt-2.7b model (~4-6GB).

## Basic Usage

```python
from vqa_model import answer_question

# Simple example
image_path = "../data/samples/image.jpg"
question = "What objects are in this image?"
answer = answer_question(image_path, question)
print(answer)
```

## Using with the Flask App

The VQA module integrates with the Flask backend:

```bash
python ../main.py
```

Then upload an image and ask a question through the web interface.

## GPU Optimization

To use GPU acceleration (requires CUDA):

```bash
# Install GPU dependencies
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Run setup to load on GPU
python setup_vqa.py
```

## Why BLIP-2?

- **Smaller:** 2.7B parameters (vs 7B for larger models)
- **Faster:** 2-5s inference on GPU, 15-20s on CPU
- **Lower Memory:** 4-6GB RAM vs 16GB for larger models
- **Better for Resource-Constrained Devices**

## Troubleshooting

- **Out of Memory:** Use CPU or reduce batch size
- **Model not found:** Run `python setup_vqa.py` to download
- **Slow inference:** Consider using GPU acceleration

See `README.md` for detailed documentation.
