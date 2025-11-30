"""Command-line entrypoint for the OCR app.

Usage examples:
  # from repo root (recommended):
  cd ocr/ocr-app/src
  python -m ocr_app.main path/to/image.jpg

  # or run the file directly (the script will try to add the src dir to PYTHONPATH):
  python ocr/ocr-app/src/ocr_app/main.py path/to/image.jpg

The CLI accepts multiple image paths and optional tesseract path overrides.
"""

import argparse
import sys
import pathlib
from typing import List

# Robust import: allow running as module (`-m ocr_app.main`) or as a script by fixing sys.path.
try:
    from ocr_app.ocr import OCR
    from ocr_app.preprocess import preprocess_image
    from ocr_app.utils import normalize_ocr
except Exception:
    # find nearest parent named 'src' and add it to sys.path
    here = pathlib.Path(__file__).resolve()
    parents = list(here.parents)
    src_dir = None
    for p in parents:
        if p.name == 'src':
            src_dir = p
            break
    if src_dir is None:
        # fallback: use parent two levels up (ocr_app -> src)
        src_dir = here.parents[1]
    sys.path.insert(0, str(src_dir))
    from ocr_app.ocr import OCR
    from ocr_app.preprocess import preprocess_image
    from ocr_app.utils import normalize_ocr


def process_images(paths: List[str], tesseract_path: str | None, lang: str, oem: int, psm: int, out_dir: str | None):
    ocr_engine = OCR(tesseract_cmd=tesseract_path, lang=lang, oem=oem, psm=psm)
    results = {}
    for p in paths:
        try:
            # Preprocess the image
            try:
                preprocessed = preprocess_image(p)
            except Exception as e:
                print(f"[OCR] Preprocessing failed, using direct load: {e}")
                preprocessed = ocr_engine.load_image(p)
            
            # Run full OCR with multi-scale processing
            raw_text = ocr_engine.full_ocr(preprocessed, scales=(1.0, 1.5, 2.0))
            
            # Try PSM trials if initial result has low confidence or is short
            if len(raw_text.strip()) < 10 or ocr_engine.last_confidence < 50:
                psm_text, psm_conf = ocr_engine._ocr_with_psm_trials(preprocessed)
                if psm_conf > 50 and len(psm_text) >= len(raw_text):
                    raw_text = psm_text
            
            # Try MSER detection if result is still short
            if len(raw_text.strip()) < 5:
                boxes = ocr_engine._detect_text_regions_mser(preprocessed)
                if boxes:
                    mser_text = ocr_engine._ocr_regions_and_merge(preprocessed, boxes)
                    if len(mser_text) > len(raw_text):
                        raw_text = mser_text
            
            # Apply spell correction and normalization
            text = normalize_ocr(raw_text)
            
            results[p] = text
            print(f"--- {p} ---")
            print(text or "(no text found)")
            if out_dir:
                out_path = pathlib.Path(out_dir) / (pathlib.Path(p).stem + ".txt")
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_text(text, encoding='utf-8')
        except Exception as e:
            print(f"Error processing {p}: {e}")
    return results


def build_arg_parser():
    p = argparse.ArgumentParser(description='OCR CLI for Assistive-VQA (ocr_app)')
    p.add_argument('images', nargs='+', help='One or more image files to run OCR on')
    p.add_argument('--tesseract-path', dest='tesseract_path', help='Full path to tesseract executable')
    p.add_argument('--lang', default='eng', help='Tesseract language code (default: eng)')
    p.add_argument('--oem', type=int, default=3, help='Tesseract OEM flag (default: 3)')
    p.add_argument('--psm', type=int, default=3, help='Tesseract PSM flag (default: 3)')
    p.add_argument('--out-dir', dest='out_dir', help='Optional directory to write extracted .txt files')
    return p


def main(argv: List[str] | None = None):
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    process_images(args.images, args.tesseract_path, args.lang, args.oem, args.psm, args.out_dir)


if __name__ == '__main__':
    main()