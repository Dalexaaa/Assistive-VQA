
"""Interactive quick inference script for VQA module.

Usage examples (PowerShell):

# Interactive mode (asks multiple questions):
# .\venv\Scripts\python.exe vqa/run_quick_inference.py ..\data/samples/sample1.jpg

# Single-shot mode (question passed as argument):
# .\venv\Scripts\python.exe vqa/run_quick_inference.py ..\data/samples/sample1.jpg "What is in the image?"

# Batch mode (questions from a text file, one per line):
# .\venv\Scripts\python.exe vqa/run_quick_inference.py ..\data/samples/sample1.jpg --questions-file questions.txt

This script loads the model once and reuses it for multiple queries. It prints timing info and returned answers.
"""

import sys
import argparse
import time
from pathlib import Path

# Ensure the project root is on sys.path so `from vqa import ...` works even when
# the script is run as `python vqa/run_quick_inference.py` from the repo root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from vqa.vqa_model import load_model, answer_question, unload_model


def main():
    parser = argparse.ArgumentParser(description="Run quick VQA inference (loads model once).")
    parser.add_argument("image", help="Path to image file")
    parser.add_argument("question", nargs="?", help="Optional single question to ask")
    parser.add_argument("--questions-file", help="Path to a text file with one question per line")
    args = parser.parse_args()

    img_path = Path(args.image)
    if not img_path.exists():
        print(f"Error: image not found: {img_path}")
        return

    # Load model once
    print("Loading VQA model (this may take a moment)...")
    model, processor, device = load_model()
    print(f"Model loaded on device: {device}")

    questions = []
    if args.question:
        questions.append(args.question)
    elif args.questions_file:
        qf = Path(args.questions_file)
        if not qf.exists():
            print(f"Questions file not found: {qf}")
            unload_model()
            return
        questions = [line.strip() for line in qf.read_text(encoding="utf-8").splitlines() if line.strip()]
    else:
        # Interactive loop
        print("Entering interactive mode. Type an empty line to exit.")
        while True:
            q = input("Question> ").strip()
            if q == "":
                break
            questions.append(q)

    for q in questions:
        print(f"\nQ: {q}")
        t0 = time.time()
        try:
            ans = answer_question(str(img_path), q)
        except Exception as e:
            print(f"Error during inference: {e}")
            continue
        t1 = time.time()
        print(f"A: {ans}")
        print(f"(inference time: {t1-t0:.2f}s)")

    unload_model()


if __name__ == "__main__":
    main()
