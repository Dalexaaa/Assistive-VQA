"""
Comprehensive Evaluation Script for Assistive-VQA System
Measures:
- VQA Model Accuracy
- OCR Model Accuracy
- Routing Logic Accuracy
- Overall System Performance
- Response Time Metrics
"""

import os
import sys
import time
import csv
import json
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import modules
try:
    from vqa.vqa_model import answer_question as vqa_answer
    VQA_AVAILABLE = True
except Exception as e:
    print(f"VQA module not available: {e}")
    VQA_AVAILABLE = False

try:
    from ocr.ocr_module import extract_text as ocr_extract
    OCR_AVAILABLE = True
except Exception as e:
    print(f"OCR module not available: {e}")
    OCR_AVAILABLE = False

try:
    from ui.app import determine_module
    ROUTING_AVAILABLE = True
except Exception as e:
    print(f"Routing module not available: {e}")
    ROUTING_AVAILABLE = False


class EvaluationMetrics:
    """Calculate and store evaluation metrics"""
    
    def __init__(self):
        self.vqa_results = []
        self.ocr_results = []
        self.routing_results = []
        self.timing_results = []
    
    def add_vqa_result(self, correct: bool, response_time: float, question: str, 
                       expected: str, actual: str):
        """Add VQA evaluation result"""
        self.vqa_results.append({
            'correct': correct,
            'response_time': response_time,
            'question': question,
            'expected': expected,
            'actual': actual
        })
    
    def add_ocr_result(self, correct: bool, response_time: float, question: str,
                      expected: str, actual: str):
        """Add OCR evaluation result"""
        self.ocr_results.append({
            'correct': correct,
            'response_time': response_time,
            'question': question,
            'expected': expected,
            'actual': actual
        })
    
    def add_routing_result(self, correct: bool, question: str, 
                          expected_module: str, actual_module: str):
        """Add routing evaluation result"""
        self.routing_results.append({
            'correct': correct,
            'question': question,
            'expected': expected_module,
            'actual': actual_module
        })
    
    def calculate_accuracy(self, results: List[Dict]) -> float:
        """Calculate accuracy percentage"""
        if not results:
            return 0.0
        correct = sum(1 for r in results if r['correct'])
        return (correct / len(results)) * 100
    
    def calculate_avg_time(self, results: List[Dict]) -> float:
        """Calculate average response time"""
        if not results:
            return 0.0
        times = [r['response_time'] for r in results if 'response_time' in r]
        return sum(times) / len(times) if times else 0.0
    
    def get_summary(self) -> Dict:
        """Get evaluation summary"""
        return {
            'vqa': {
                'accuracy': self.calculate_accuracy(self.vqa_results),
                'avg_time': self.calculate_avg_time(self.vqa_results),
                'total_tests': len(self.vqa_results),
                'correct': sum(1 for r in self.vqa_results if r['correct'])
            },
            'ocr': {
                'accuracy': self.calculate_accuracy(self.ocr_results),
                'avg_time': self.calculate_avg_time(self.ocr_results),
                'total_tests': len(self.ocr_results),
                'correct': sum(1 for r in self.ocr_results if r['correct'])
            },
            'routing': {
                'accuracy': self.calculate_accuracy(self.routing_results),
                'total_tests': len(self.routing_results),
                'correct': sum(1 for r in self.routing_results if r['correct'])
            },
            'overall': {
                'total_tests': len(self.vqa_results) + len(self.ocr_results),
                'total_correct': sum(1 for r in self.vqa_results if r['correct']) + 
                               sum(1 for r in self.ocr_results if r['correct'])
            }
        }


def check_answer_similarity(expected: str, actual: str, threshold: float = 0.6) -> bool:
    """
    Check if actual answer is similar enough to expected answer
    Uses simple word matching for evaluation
    """
    if not expected or not actual:
        return False
    
    # Normalize strings
    expected_lower = expected.lower().strip()
    actual_lower = actual.lower().strip()
    
    # Exact match
    if expected_lower == actual_lower:
        return True
    
    # Check if expected is contained in actual (common for VQA)
    if expected_lower in actual_lower:
        return True
    
    # Word-level matching
    expected_words = set(expected_lower.split())
    actual_words = set(actual_lower.split())
    
    if not expected_words:
        return False
    
    # Calculate word overlap
    overlap = len(expected_words & actual_words)
    similarity = overlap / len(expected_words)
    
    return similarity >= threshold


def evaluate_test_cases(csv_path: str, metrics: EvaluationMetrics) -> None:
    """Evaluate all test cases from CSV file"""
    
    if not os.path.exists(csv_path):
        print(f"Test cases file not found: {csv_path}")
        return
    
    print(f"\n{'='*70}")
    print(f"Evaluating test cases from: {csv_path}")
    print(f"{'='*70}\n")
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        test_cases = list(reader)
    
    for i, case in enumerate(test_cases, 1):
        image_path = case.get('image_path', '').strip()
        question = case.get('question', '').strip()
        expected_module = case.get('expected_module', '').strip().lower()
        expected_output = case.get('expected_output', '').strip()
        notes = case.get('notes', '').strip()
        
        if not image_path or not question:
            continue
        
        print(f"\n{'─'*70}")
        print(f"Test Case {i}: {notes}")
        print(f"{'─'*70}")
        print(f"Image: {image_path}")
        print(f"Question: {question}")
        print(f"Expected Module: {expected_module.upper()}")
        print(f"Expected Output: {expected_output}")
        
        # Full path to image
        full_image_path = os.path.join(project_root, image_path)
        
        # Test 1: Routing Logic
        if ROUTING_AVAILABLE:
            actual_module = determine_module(question)
            routing_correct = (actual_module == expected_module)
            metrics.add_routing_result(routing_correct, question, expected_module, actual_module)
            
            status = "Correct" if routing_correct else "Incorrect"
            print(f"{status} Routing: {actual_module.upper()} (Expected: {expected_module.upper()})")
        else:
            print("Routing: Not available")
        
        # Test 2: Module Execution
        if expected_module == 'vqa' and VQA_AVAILABLE:
            if os.path.exists(full_image_path):
                try:
                    start_time = time.time()
                    actual_output = vqa_answer(full_image_path, question)
                    response_time = time.time() - start_time
                    
                    correct = check_answer_similarity(expected_output, actual_output)
                    metrics.add_vqa_result(correct, response_time, question, 
                                          expected_output, actual_output)
                    
                    status = "Correct" if correct else "Incorrect"
                    print(f"{status} VQA Output: {actual_output}")
                    print(f"Response Time: {response_time:.2f}s")
                except Exception as e:
                    print(f"VQA Error: {e}")
                    metrics.add_vqa_result(False, 0, question, expected_output, str(e))
            else:
                print(f"Image not found: {full_image_path}")
        
        elif expected_module == 'ocr' and OCR_AVAILABLE:
            if os.path.exists(full_image_path):
                try:
                    start_time = time.time()
                    actual_output = ocr_extract(full_image_path)
                    response_time = time.time() - start_time
                    
                    correct = check_answer_similarity(expected_output, actual_output)
                    metrics.add_ocr_result(correct, response_time, question,
                                          expected_output, actual_output)
                    
                    status = "Correct" if correct else "Incorrect"
                    print(f"{status} OCR Output: {actual_output}")
                    print(f"Response Time: {response_time:.2f}s")
                except Exception as e:
                    print(f"OCR Error: {e}")
                    metrics.add_ocr_result(False, 0, question, expected_output, str(e))
            else:
                print(f"Image not found: {full_image_path}")


def print_summary(metrics: EvaluationMetrics) -> None:
    """Print evaluation summary"""
    summary = metrics.get_summary()
    
    print(f"\n{'='*70}")
    print(f"EVALUATION SUMMARY")
    print(f"{'='*70}\n")
    
    # VQA Metrics
    print(f"VQA MODULE:")
    print(f"   Accuracy: {summary['vqa']['accuracy']:.1f}% "
          f"({summary['vqa']['correct']}/{summary['vqa']['total_tests']})")
    if summary['vqa']['avg_time'] > 0:
        print(f"   Avg Response Time: {summary['vqa']['avg_time']:.2f}s")
    print()
    
    # OCR Metrics
    print(f"OCR MODULE:")
    print(f"   Accuracy: {summary['ocr']['accuracy']:.1f}% "
          f"({summary['ocr']['correct']}/{summary['ocr']['total_tests']})")
    if summary['ocr']['avg_time'] > 0:
        print(f"   Avg Response Time: {summary['ocr']['avg_time']:.2f}s")
    print()
    
    # Routing Metrics
    print(f"ROUTING LOGIC:")
    print(f"   Accuracy: {summary['routing']['accuracy']:.1f}% "
          f"({summary['routing']['correct']}/{summary['routing']['total_tests']})")
    print()
    
    # Overall Metrics
    if summary['overall']['total_tests'] > 0:
        overall_accuracy = (summary['overall']['total_correct'] / 
                          summary['overall']['total_tests']) * 100
        print(f"OVERALL SYSTEM:")
        print(f"   Accuracy: {overall_accuracy:.1f}% "
              f"({summary['overall']['total_correct']}/{summary['overall']['total_tests']})")
    
    print(f"\n{'='*70}\n")


def save_results(metrics: EvaluationMetrics, output_file: str = "evaluation_results.json") -> None:
    """Save detailed results to JSON file"""
    results = {
        'timestamp': datetime.now().isoformat(),
        'summary': metrics.get_summary(),
        'vqa_details': metrics.vqa_results,
        'ocr_details': metrics.ocr_results,
        'routing_details': metrics.routing_results
    }
    
    output_path = os.path.join(project_root, output_file)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"Detailed results saved to: {output_file}")


def main():
    """Main evaluation function"""
    print(f"\n{'='*70}")
    print(f"ASSISTIVE-VQA SYSTEM EVALUATION")
    print(f"{'='*70}\n")
    
    # Check module availability
    print("Module Availability:")
    print(f"   VQA: {'Available' if VQA_AVAILABLE else 'Not Available'}")
    print(f"   OCR: {'Available' if OCR_AVAILABLE else 'Not Available'}")
    print(f"   Routing: {'Available' if ROUTING_AVAILABLE else 'Not Available'}")
    
    if not (VQA_AVAILABLE or OCR_AVAILABLE):
        print("\nNo modules available for evaluation. Exiting.")
        return
    
    # Initialize metrics
    metrics = EvaluationMetrics()
    
    # Evaluate test cases
    csv_path = os.path.join(project_root, 'data', 'cases.csv')
    evaluate_test_cases(csv_path, metrics)
    
    # Print summary
    print_summary(metrics)
    
    # Save results
    save_results(metrics)
    
    print("Evaluation complete!\n")


if __name__ == "__main__":
    main()
