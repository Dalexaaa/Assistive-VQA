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
"""VQA module README

This file documents how to install, run, and troubleshoot the VQA module that uses
the BLIP-2 model (`Salesforce/blip2-opt-2.7b`).
"""

# VQA Module (BLIP-2)

**Status:** Implemented (model: `Salesforce/blip2-opt-2.7b`)

This package provides a small API to perform Visual Question Answering using BLIP-2.

**Files of interest:**
- `vqa_model.py` — core functions: `load_model()`, `answer_question(image_path, question)`, `unload_model()`
- `setup_vqa.py` — helper that downloads the model and verifies it loads correctly
- `test_vqa.py` — unit tests for the module

**Quickstart**

1. Create and activate a virtual environment (PowerShell example):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
```

2. Install dependencies. Install non-PyTorch deps from the project `requirements.txt`, then install PyTorch using the official instructions for your platform (CPU/CUDA).

```powershell
python -m pip install -r requirements.txt

# Example CPU-only PyTorch install (adjust for CUDA if you have a GPU):
python -m pip install "torch==2.9.1+cpu" torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

3. Download and verify the model (runs once):

```powershell
python vqa\setup_vqa.py
```

4. Run tests:

```powershell
python -m pytest -q vqa\test_vqa.py
```

5. Quick ad-hoc inference (Python example):

```python
from vqa.vqa_model import answer_question
print(answer_question(r"data/samples/sample.jpg", "What is in this image?"))
```

Or from the shell:

```powershell
.\venv\Scripts\python.exe -c "from vqa.vqa_model import answer_question; print(answer_question(r'data/samples/sample.jpg','What is in this image?'))"
```

Integration
- The Flask UI can call `vqa.vqa_model.answer_question(image_path, question)` to serve VQA responses.
- Example HTTP (POST) to a running endpoint:

```bash
curl -X POST http://localhost:5001/api/query -F "image=@test.jpg" -F "question=What is in this image?"
```

Notes & Troubleshooting
- Model download: expect several GB of download and cache. Ensure sufficient disk space.
- Hugging Face cache on Windows may warn about symlink support; this is informational. To silence: set `HF_HUB_DISABLE_SYMLINKS_WARNING=1`.
- Non-fatal warnings such as ``torch_dtype is deprecated`` are safe to ignore; they don't prevent operation.
- If you experience OOM errors:
  - Use GPU if available and ensure `torch` matches your CUDA version.
  - Try float16 inference or model offloading techniques.
  - Reduce batch sizes and clear cache with `torch.cuda.empty_cache()`.
- If model download fails:
  - Verify internet and disk space
  - Authenticate with Hugging Face if required: `huggingface-cli login`

If you want a smaller memory footprint we can switch to a smaller BLIP model variant or add explicit offloading in `vqa_model.py`.

References
- BLIP-2: https://huggingface.co/Salesforce/blip2-opt-2.7b
- Hugging Face Transformers: https://huggingface.co/docs/transformers
