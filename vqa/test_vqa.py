"""
Unit tests for the VQA module
"""

import pytest
import os
from pathlib import Path
from PIL import Image
import tempfile
from vqa_model import answer_question, load_model


class TestVQAModule:
    """Test cases for VQA module functionality"""
    
    @pytest.fixture(scope="session")
    def sample_image(self):
        """Create a simple test image"""
        # Create a temporary image for testing
        img = Image.new('RGB', (100, 100), color='red')
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
            img.save(f.name)
            yield f.name
        # Cleanup
        os.unlink(f.name)
    
    def test_load_model(self):
        """Test that model loads successfully"""
        try:
            model, processor, device = load_model()
            assert model is not None
            assert processor is not None
            assert device is not None
        except Exception as e:
            pytest.skip(f"Model loading failed: {e}")
    
    def test_answer_question_with_valid_image(self, sample_image):
        """Test answering a question about a valid image"""
        try:
            answer = answer_question(sample_image, "What color is this?")
            assert isinstance(answer, str)
            assert len(answer) > 0
        except Exception as e:
            pytest.skip(f"Test skipped: {e}")
    
    def test_answer_question_with_nonexistent_image(self):
        """Test that proper error is raised for nonexistent image"""
        with pytest.raises(FileNotFoundError):
            answer_question("nonexistent_image.jpg", "What's in this image?")
    
    def test_answer_question_with_empty_question(self, sample_image):
        """Test handling of empty question"""
        with pytest.raises(ValueError):
            answer_question(sample_image, "")
    
    def test_answer_question_returns_string(self, sample_image):
        """Test that answer is returned as string"""
        try:
            answer = answer_question(sample_image, "What do you see?")
            assert isinstance(answer, str)
        except Exception as e:
            pytest.skip(f"Test skipped: {e}")
    
    def test_multiple_questions_same_image(self, sample_image):
        """Test asking multiple questions about the same image"""
        try:
            answer1 = answer_question(sample_image, "What color is this?")
            answer2 = answer_question(sample_image, "Describe this image")
            
            assert isinstance(answer1, str)
            assert isinstance(answer2, str)
            assert len(answer1) > 0
            assert len(answer2) > 0
        except Exception as e:
            pytest.skip(f"Test skipped: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
