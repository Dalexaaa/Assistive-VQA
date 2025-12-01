# Visual Question Answering (VQA) Module

**Status:** Implemented and in testing for better accuracy  
**Model:** `Salesforce/blip2-opt-2.7b` (2.7B parameters)  
**Platforms:** Windows, macOS, Linux  
**Hardware:** GPU recommended (tested on NVIDIA RTX 3080 Ti)

---

## Overview

The VQA module analyzes images and answers natural language questions about visual content using the BLIP-2-opt-2.7b vision-language model. It provides a simple, production-ready API with batch evaluation capabilities.

**Key features:**
- Single-image inference via `answer_question(image_path, question)`
- Batch evaluation with accuracy metrics (exact-match, token-overlap, sequence-similarity)
- GPU acceleration (CUDA) or CPU fallback
- Comprehensive testing and evaluation framework

---

## Quick Start

### 1. Install Dependencies

Create and activate a Python virtual environment:

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
```

### 2. Install PyTorch (Platform-Specific)

Install PyTorch FIRST, then other dependencies:

**CPU-only (Windows/macOS/Linux):**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

**GPU with CUDA 12.1 (Windows/Linux only):**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

**GPU with CUDA 11.8 (Windows/Linux only):**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**Apple Silicon GPU (M1/M2/M3, macOS only):**
```bash
pip install torch torchvision torchaudio
```

### 3. Install Other Dependencies

```bash
pip install -r vqa/requirements.txt
```

### 4. Download the Model

Run the setup script (first time only):

```bash
python vqa/setup_vqa.py
```

This downloads the BLIP-2 model (~4-6 GB) and caches it locally. On subsequent runs, the cached model is used.

### 5. Verify Installation

Run the unit tests:

```bash
python -m pytest vqa/test_vqa.py -v
```

Expected output: **6 tests passed**

---

## How to Use

### Single Image Inference

**Python API:**

```python
from vqa.vqa_model import answer_question, load_model, unload_model

# Optional: explicitly load model
load_model()

# Answer a question about an image
answer = answer_question("path/to/image.jpg", "What is in this image?")
print(answer)

# Optional: free GPU memory when done
unload_model()
```

**Command line:**

```powershell
python -c "from vqa.vqa_model import answer_question; print(answer_question('data/samples/sample.jpg', 'What is in this image?'))"
```

### Interactive Mode

Test the model interactively on multiple images:

```bash
python vqa/testing/run_quick_inference.py
```

Choose mode:
- **Interactive (1):** Loop through questions until you exit
- **Single (2):** Answer one question and exit
- **Batch (3):** Process questions from a file (one per line)

### Batch Evaluation

Evaluate the model on a test dataset and get accuracy metrics:

```bash
# Default: reads validation_set.json, outputs JSON results to vqa/testing/results/
python vqa/testing/evaluate.py

# Custom input/output paths
python vqa/testing/evaluate.py --data data/validation_set.json --output my_results.json

# CSV format also supported
python vqa/testing/evaluate.py --data data/cases.csv --output results.json
```

**Output format:** JSON file with metadata, summary metrics, and per-sample results:

```json
{
  "metadata": {
    "timestamp": "2024-01-15T10:30:45",
    "total_samples": 100,
    "evaluation_time_seconds": 125.5
  },
  "summary": {
    "exact_match_accuracy": 0.45,
    "token_overlap_accuracy": 0.62,
    "sequence_similarity_accuracy": 0.58,
    "average_inference_time_seconds": 1.25
  },
  "results": [
    {
      "image_path": "data/validation_set/image_001.jpg",
      "question": "What color is the car?",
      "predicted_answer": "The car is red",
      "reference_answers": ["red car", "red vehicle"],
      "inference_time_seconds": 1.23,
      "metrics": {
        "exact_match": false,
        "token_overlap": 0.5,
        "sequence_similarity": 0.67
      }
    }
  ]
}
```

---

## File Structure

```
vqa/
├── README.md                    # This file (you are here)
├── requirements.txt             # Python dependencies (PyTorch installed separately)
├── vqa_model.py                # Core VQA module (main API)
├── setup_vqa.py                # Model download and verification
├── test_vqa.py                 # Unit tests (6 tests, all passing)
└── testing/
    ├── README.md               # Testing and evaluation guide
    ├── evaluate.py            # Batch evaluation harness with metrics
    ├── run_quick_inference.py # Interactive/batch inference tool
    └── results/               # Output directory for evaluation results
        └── evaluation_results_*.json  # Saved evaluation output
```

---

## API Reference

### `vqa_model.py`

#### `load_model() → None`

Load the BLIP-2 model into memory. Called automatically by `answer_question()` if not already loaded.

```python
from vqa.vqa_model import load_model
load_model()  # GPU memory allocated here
```

#### `answer_question(image_path: str, question: str) → str`

Answer a question about an image.

| Parameter | Type | Description |
|-----------|------|-------------|
| `image_path` | `str` | Path to image file (JPG, PNG, etc.) |
| `question` | `str` | Natural language question |
| **Returns** | `str` | Model's answer |

```python
from vqa.vqa_model import answer_question

answer = answer_question("image.jpg", "What is the weather?")
# Output: "The weather is sunny with clear blue skies"
```

#### `unload_model() → None`

Free GPU memory and unload the model.

```python
from vqa.vqa_model import unload_model
unload_model()  # GPU memory released
```

---

## Model Details

### BLIP-2-opt-2.7b

- **Type:** Vision-language transformer
- **Architecture:** BLIP vision encoder + OPT-2.7B language decoder
- **Size:** 2.7 billion parameters
- **Inference:** ~1–2 seconds per question (GPU), ~5–10 seconds (CPU)
- **Memory:** ~6 GB (GPU), ~8 GB (CPU)
- **Strengths:** Fast, lightweight, good visual understanding
- **Limitations:** May echo questions or produce incomplete answers (mitigated by post-processing)

### Generation Parameters

The model is configured with:

```python
generation_kwargs = {
    "max_new_tokens": 64,           # Limit answer length
    "num_beams": 3,                 # Beam search for better quality
    "no_repeat_ngram_size": 3,      # Avoid repetition
    "early_stopping": True,          # Stop when confident
}
```

### Prompting

Questions are formatted as:

```
Question: {question_text}
Answer:
```

Post-processing removes echoed questions and "Answer:" markers from the response.

---

## Performance

### Inference Speed

- **GPU (NVIDIA RTX 3080 Ti):** ~0.5–1.5 seconds per image
- **GPU (NVIDIA RTX 3060):** ~1–2 seconds per image
- **CPU (Intel i7-12700K):** ~5–10 seconds per image

### Accuracy

Depends on image complexity and question clarity:

- **Simple questions** (e.g., "What color is the car?"): 70–85% exact match
- **Complex questions** (e.g., "What activities are people doing?"): 40–60% exact match
- **Fuzzy match** (token overlap): 60–75%

*Note: Accuracy is dataset-dependent. See evaluation results for your specific data.*

---

## Configuration

### Environment Variables

**Windows (PowerShell):**
```powershell
$env:HF_HOME = "C:\Models"                          # Model cache location
$env:HF_HUB_DISABLE_SYMLINKS_WARNING = "1"         # Suppress Windows symlink warnings
$env:TRANSFORMERS_VERBOSITY = "error"               # Log level
```

**macOS/Linux (Bash):**
```bash
export HF_HOME="$HOME/models"                      # Model cache location
export HF_HUB_DISABLE_SYMLINKS_WARNING="1"         # Optional
export TRANSFORMERS_VERBOSITY="error"              # Log level: quiet, error, warning, info, debug
```

### Model Configuration

To use a different BLIP-2 variant, edit `vqa_model.py`:

```python
# Line ~15 in vqa_model.py
MODEL_ID = "Salesforce/blip2-opt-2.7b"  # Change to:
# "Salesforce/blip2-opt-6.7b"  # Larger model, slower but better quality
# "Salesforce/blip2-opt-2.7b-ib"  # Intermediate-budget variant
```

---

## Troubleshooting

### Common Issues

#### Model Download Fails

**Problem:** `ConnectionError` or timeout during model download

**Solution (Windows):**
```powershell
Test-NetConnection huggingface.co -Port 443
pip install huggingface-hub
huggingface-cli login
python vqa/setup_vqa.py
```

**Solution (macOS/Linux):**
```bash
ping -c 3 huggingface.co
pip install huggingface-hub
huggingface-cli login
python vqa/setup_vqa.py
```

#### CUDA Out of Memory (OOM)

**Problem:** `RuntimeError: CUDA out of memory`

**Solution:**
```python
# Option 1: Use CPU
import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""

# Option 2: Clear cache before inference
import torch
torch.cuda.empty_cache()

# Option 3: Use a smaller model variant
# Edit vqa_model.py, change MODEL_ID to "Salesforce/blip2-opt-2.7b"
```

#### Model Not Found / Import Errors

**Problem:** `ModuleNotFoundError: No module named 'vqa'`

**Solution (Windows):**
```powershell
cd c:\path\to\Assistive-VQA
.\venv\Scripts\Activate.ps1
python -m pip install -r vqa/requirements.txt
```

**Solution (macOS/Linux):**
```bash
cd /path/to/Assistive-VQA
source venv/bin/activate
python -m pip install -r vqa/requirements.txt
```

#### Slow Inference

**Problem:** Inference takes >5 seconds per image

**Solution:**
1. Verify GPU is being used:
   ```python
   from vqa.vqa_model import get_device
   print(get_device())  # Should print 'cuda' not 'cpu'
   ```
2. Check GPU availability:
   ```python
   import torch
   print(f"CUDA available: {torch.cuda.is_available()}")
   print(f"GPU: {torch.cuda.get_device_name(0)}")
   ```
3. If on CPU, reinstall PyTorch for your CUDA version (see [Install Dependencies](#1-install-dependencies))

#### Strange Answers or Question Echoing

**Problem:** Model answers include the question text

**Solution:** This is normal for BLIP-2. The `answer_question()` function includes post-processing to strip echoes. If echoes persist:

1. Update `vqa/vqa_model.py` to `vqa_model.py` line ~60 (check post-processing logic)
2. Increase `max_new_tokens` or adjust beam search parameters

---

## Testing & Evaluation

See [vqa/testing/README.md](testing/README.md) for detailed testing instructions.

**Quick test:**

```bash
# Run unit tests
python -m pytest vqa/test_vqa.py -v

# Run batch evaluation on validation dataset
python vqa/testing/evaluate.py

# Run interactive inference
python vqa/testing/run_quick_inference.py
```

---

## Integration Examples

### Flask Web Service

The VQA module is designed to work with a Flask UI. Example endpoint:

```python
from flask import Flask, request
from vqa.vqa_model import answer_question

app = Flask(__name__)

@app.route('/api/vqa', methods=['POST'])
def vqa_endpoint():
    image_file = request.files['image']
    question = request.form['question']
    
    # Save temp image
    image_path = '/tmp/temp_image.jpg'
    image_file.save(image_path)
    
    # Get answer
    answer = answer_question(image_path, question)
    
    return {'answer': answer}
```

### Batch Processing

Process a large number of images:

```python
from vqa.vqa_model import load_model, answer_question, unload_model
import glob

load_model()

for image_path in glob.glob("data/images/*.jpg"):
    question = "What is in this image?"
    answer = answer_question(image_path, question)
    print(f"{image_path}: {answer}")

unload_model()
```

---

## Requirements

### System Requirements

**Operating System:**
- Windows 10/11 (64-bit)
- macOS 11+ (Intel or Apple Silicon)
- Linux (Ubuntu 18.04+, etc.)

**Hardware:**
- **Python:** 3.8+
- **RAM:** 8 GB minimum (16 GB recommended)
- **GPU (optional but recommended):**
  - **NVIDIA:** CUDA 11.8+ with cuDNN 8.6+, 6 GB VRAM minimum
  - **Apple Silicon:** Built-in GPU support (M1/M2/M3)
  - **No GPU:** CPU fallback supported (~5-10s per image)

**Disk Space:**
- Model cache: ~4-6 GB
- Python packages: ~1-2 GB
- Evaluation results: ~100-500 MB

### Python Dependencies

See `requirements.txt` for the complete list and installation instructions.

**Core Packages:**
- **torch** (≥2.0) — Deep learning framework (install separately per platform)
- **torchvision** — Computer vision utilities
- **transformers** (≥4.30) — Hugging Face model hub and inference
- **accelerate** — Distributed training & mixed precision
- **Pillow** (≥10.0) — Image I/O and processing
- **numpy** (≥1.24) — Numerical computing
- **scipy** (≥1.10) — Scientific metrics

**Development & Testing:**
- **pytest** (≥7.0) — Unit testing framework
- **pytest-cov** — Code coverage reporting
- **psutil** — System resource monitoring

---

## References

- **BLIP-2 Model:** https://huggingface.co/Salesforce/blip2-opt-2.7b
- **Hugging Face Transformers:** https://huggingface.co/docs/transformers/
- **PyTorch:** https://pytorch.org/
- **BLIP-2 Paper:** https://arxiv.org/abs/2301.12597

---
