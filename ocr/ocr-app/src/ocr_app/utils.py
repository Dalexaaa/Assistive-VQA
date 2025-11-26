"""Utility helpers for OCR post-processing and small corrections."""
from typing import Iterable


def _levenshtein(a: str, b: str) -> int:
    # simple iterative DP implementation
    if a == b:
        return 0
    la, lb = len(a), len(b)
    if la == 0:
        return lb
    if lb == 0:
        return la
    prev = list(range(lb + 1))
    for i, ca in enumerate(a, start=1):
        cur = [i] + [0] * lb
        for j, cb in enumerate(b, start=1):
            cost = 0 if ca == cb else 1
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost)
        prev = cur
    return prev[lb]


def normalize_ocr(text: str, candidates: Iterable[str] | None = None) -> str:
    """Apply simple normalizations and optionally correct to a close candidate.

    - Uppercases result
    - Replaces common digit/letter confusions
    - If `candidates` provided, and a candidate is within edit distance 1-2, replace with it.
    """
    if not text:
        return text
    s = text.strip().upper()

    # digit -> letter mappings commonly confused by OCR
    mapping = str.maketrans({
        '0': 'O',
        '1': 'I',
        '5': 'S',
        '2': 'Z',
        '8': 'B'
    })
    s = s.translate(mapping)

    # trim non-alpha around words
    s = ''.join(ch for ch in s if ch.isalnum() or ch.isspace())
    s = ' '.join(s.split())

    if candidates:
        best = s
        best_dist = None
        for c in candidates:
            d = _levenshtein(s, c.upper())
            if best_dist is None or d < best_dist:
                best = c.upper()
                best_dist = d
        # accept small corrections only
        if best_dist is not None and best_dist <= 1:
            return best

    return s
def log_message(message):
    print(f"[LOG] {message}")

def handle_error(error):
    print(f"[ERROR] {error}")

def display_image(image):
    import cv2
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()