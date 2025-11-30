"""
VQA Module - Visual Question Answering using BLIP-2
Implements visual question answering using the BLIP-2-opt-2.7b model.
"""

import torch
from transformers import Blip2Processor, Blip2ForConditionalGeneration
from PIL import Image
import os
from pathlib import Path

# Global model and processor instances (loaded once)
_model = None
_processor = None
_device = None


def get_device():
    """
    Get the appropriate device (CUDA, MPS, or CPU).
    
    Returns:
        torch.device: The device to use for model inference
    """
    global _device
    
    if _device is None:
        if torch.cuda.is_available():
            _device = torch.device("cuda")
            print(f"Using CUDA device: {torch.cuda.get_device_name(0)}")
        elif torch.backends.mps.is_available():
            _device = torch.device("mps")
            print("Using Apple MPS device")
        else:
            _device = torch.device("cpu")
            print("Using CPU device")
    
    return _device


def load_model():
    """
    Load the BLIP-2-opt-2.7b model and processor.
    Uses caching to avoid reloading the model.
    
    Returns:
        tuple: (model, processor, device)
    """
    global _model, _processor, _device
    
    if _model is not None:
        return _model, _processor, _device
    
    print("Loading BLIP-2-opt-2.7b model...")
    
    device = get_device()
    model_id = "Salesforce/blip2-opt-2.7b"
    
    try:
        # Load processor
        _processor = Blip2Processor.from_pretrained(model_id)
        
        # Load model with appropriate settings
        if device.type == "cuda":
            _model = Blip2ForConditionalGeneration.from_pretrained(
                model_id,
                torch_dtype=torch.float16,
                device_map="auto"
            )
        else:
            _model = Blip2ForConditionalGeneration.from_pretrained(
                model_id,
                device_map=device
            )
        
        _model.eval()
        print(f"Model loaded successfully on {device}")
        return _model, _processor, device
        
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        raise


def answer_question(image_path: str, question: str) -> str:
    """
    Answer a visual question about an image using BLIP-2-opt-2.7b model.
    
    Args:
        image_path (str): Path to the image file
        question (str): The question to answer about the image
        
    Returns:
        str: The answer to the question
        
    Raises:
        FileNotFoundError: If the image file doesn't exist
        ValueError: If the question is empty
    """
    # Validate inputs
    if not isinstance(image_path, (str, Path)):
        raise ValueError("image_path must be a string or Path object")
    
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    if not question or not question.strip():
        raise ValueError("Question cannot be empty")
    
    try:
        # Load model if not already loaded
        model, processor, device = load_model()
        
        # Load and prepare image
        image = Image.open(image_path).convert('RGB')
        
        # Prepare a clearer instruction-style prompt to avoid the model echoing the question
        prompt = f"Question: {question}\nAnswer:"

        # Prepare inputs for BLIP-2
        inputs = processor(images=image, text=prompt, return_tensors="pt").to(device)

        # Generate answer with safer decoding parameters
        # - use max_new_tokens to limit generated tokens (preferable to max_length)
        # - use beam search for more stable outputs
        # - prevent short n-gram repetition
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=64,
                num_beams=3,
                no_repeat_ngram_size=3,
                early_stopping=True
            )

        # Decode the answer text
        # Use batch decode for consistency
        answer = processor.batch_decode(outputs, skip_special_tokens=True)[0].strip()

        # Post-process: if model echoed the question/prompt, remove the prompt portion
        if answer.lower().startswith(f"question: {question.lower()}"):
            # remove the repeated question portion
            answer = answer[len(f"question: {question}"):].strip(' :\n')
        # If the model left the literal 'Answer:' marker, strip it
        if answer.lower().startswith("answer:"):
            answer = answer[len("answer:"):].strip(' :\n')
        
        return answer if answer else "Unable to generate a response."
        
    except FileNotFoundError as e:
        return f"Error: {str(e)}"
    except ValueError as e:
        return f"Validation Error: {str(e)}"
    except Exception as e:
        return f"VQA Processing Error: {str(e)}"


def unload_model():
    """
    Unload the model to free GPU memory.
    Useful for cleanup or switching models.
    """
    global _model, _processor, _device
    
    if _model is not None:
        del _model
        _model = None
    
    if _processor is not None:
        del _processor
        _processor = None
    
    # Clear GPU cache if using CUDA
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    
    print("Model unloaded.")


if __name__ == "__main__":
    # Example usage
    import sys
    
    # Test with a sample image
    test_image = "test_image.jpg"
    test_question = "What is in this image?"
    
    if len(sys.argv) > 1:
        test_image = sys.argv[1]
    
    if len(sys.argv) > 2:
        test_question = sys.argv[2]
    
    if os.path.exists(test_image):
        try:
            answer = answer_question(test_image, test_question)
            print(f"Question: {test_question}")
            print(f"Answer: {answer}")
        except Exception as e:
            print(f"Error: {str(e)}")
    else:
        print(f"Test image not found: {test_image}")
        print("Usage: python vqa_model.py <image_path> <question>")

