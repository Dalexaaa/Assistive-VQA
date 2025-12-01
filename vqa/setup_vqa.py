"""
VQA Module Setup Script
Downloads and initializes the BLIP-2-opt-2.7b model
"""

import torch
from transformers import Blip2Processor, Blip2ForConditionalGeneration
import os

def setup_model():
    """
    Download and cache the BLIP-2-opt-2.7b model.
    This should be run once before using the VQA module.
    """
    print("Downloading BLIP-2-opt-2.7b model...")
    print("This may take a few minutes (model size: ~4-6GB)")
    
    try:
        # Load model and processor (will download from Hugging Face)
        model_id = "Salesforce/blip2-opt-2.7b"
        
        print(f"Loading processor from {model_id}...")
        processor = Blip2Processor.from_pretrained(model_id)
        print("✓ Processor loaded successfully")
        
        print(f"Loading model from {model_id}...")
        # Load in half precision for memory efficiency
        model = Blip2ForConditionalGeneration.from_pretrained(
            model_id,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        print("✓ Model loaded successfully")
        
        print("\n✓ Setup complete! VQA module is ready to use.")
        return True
        
    except Exception as e:
        print(f"✗ Error during setup: {e}")
        return False

if __name__ == "__main__":
    setup_model()
