"""
Flask API Backend for Assistive VQA
Handles image upload, question processing, and routing between VQA and OCR modules.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
from PIL import Image
import io
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for Next.js frontend

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size


def determine_module(question):
    """
    Determine whether to use OCR or VQA based on the question.
    
    Args:
        question (str): User's question about the image
        
    Returns:
        str: 'ocr' or 'vqa'
    """
    # Convert to lowercase for easier matching
    q_lower = question.lower()
    
    # OCR keywords - questions about text content
    ocr_keywords = [
        'read', 'text', 'says', 'written', 'word', 'letter',
        'sign', 'label', 'caption', 'title', 'heading',
        'number', 'digit', 'price', 'address', 'phone',
        'email', 'url', 'date', 'name on', 'writing'
    ]
    
    # VQA keywords - questions about visual content
    vqa_keywords = [
        'what color', 'how many', 'where is', 'who is',
        'what is', 'describe', 'show', 'look like',
        'doing', 'wearing', 'holding', 'scene',
        'background', 'object', 'person', 'animal'
    ]
    
    # Check for OCR keywords
    ocr_score = sum(1 for keyword in ocr_keywords if keyword in q_lower)
    
    # Check for VQA keywords
    vqa_score = sum(1 for keyword in vqa_keywords if keyword in q_lower)
    
    # Default to VQA if no clear match
    if ocr_score > vqa_score:
        return 'ocr'
    else:
        return 'vqa'


def process_with_ocr(image_path, question):
    """
    Process image using OCR module.
    
    Args:
        image_path (str): Path to the uploaded image
        question (str): User's question
        
    Returns:
        str: OCR result or answer
    """
    try:
        # Try to import OCR module
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        
        print(f"[DEBUG] Python: {sys.executable}")
        print(f"[DEBUG] OCR image_path: {image_path}")
        print(f"[DEBUG] Image exists: {os.path.exists(image_path)}")
        
        try:
            # Import and check numpy version
            import numpy as np
            print(f"[DEBUG] NumPy version: {np.__version__}")
            
            from ocr.ocr_module import extract_text
            text = extract_text(image_path)
            print(f"[DEBUG] OCR result: {text}")
            return text if text else "No text found in the image."
        except ImportError as ie:
            print(f"[DEBUG] Import error: {ie}")
            import traceback
            traceback.print_exc()
            # OCR module not yet implemented - return placeholder
            return "OCR module is being implemented. Placeholder: Text extraction from image."
    except Exception as e:
        print(f"[DEBUG] OCR Exception: {e}")
        import traceback
        traceback.print_exc()
        return f"OCR Error: {str(e)}"


def process_with_vqa(image_path, question):
    """
    Process image and question using VQA module.
    
    Args:
        image_path (str): Path to the uploaded image
        question (str): User's question
        
    Returns:
        str: Answer from VQA model
    """
    try:
        # Try to import VQA module
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        
        print(f"[DEBUG] VQA Python: {sys.executable}")
        print(f"[DEBUG] VQA image_path: {image_path}")
        print(f"[DEBUG] VQA question: {question}")
        print(f"[DEBUG] Image exists: {os.path.exists(image_path)}")
        
        try:
            from vqa.vqa_model import answer_question
            print("[DEBUG] VQA module imported successfully")
            answer = answer_question(image_path, question)
            print(f"[DEBUG] VQA result: {answer}")
            return answer if answer else "Unable to answer the question."
        except ImportError as ie:
            print(f"[DEBUG] VQA Import error: {ie}")
            import traceback
            traceback.print_exc()
            # VQA module not yet implemented - return placeholder
            return "VQA module is being implemented. Please ensure all dependencies are installed."
    except Exception as e:
        print(f"[DEBUG] VQA Exception: {e}")
        import traceback
        traceback.print_exc()
        return f"VQA Error: {str(e)}"


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'message': 'Assistive VQA API is running'
    })


@app.route('/api/query', methods=['POST'])
def query_image():
    """
    Main endpoint for processing image and question.
    
    Expects:
        - image: base64 encoded image or file upload
        - question: text question about the image
        
    Returns:
        JSON with answer, module used, and metadata
    """
    try:
        print("[API] Received request to /api/query")
        
        # Get question from request
        question = request.form.get('question', '')
        print(f"[API] Question: {question}")
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        # Get image from request
        image_data = None
        image_path = None
        
        # Check for base64 encoded image
        if 'image_base64' in request.form:
            try:
                image_b64 = request.form['image_base64']
                # Remove data URL prefix if present
                if ',' in image_b64:
                    image_b64 = image_b64.split(',')[1]
                
                image_bytes = base64.b64decode(image_b64)
                image = Image.open(io.BytesIO(image_bytes))
                
                # Save temporary file
                temp_filename = f"temp_{os.urandom(8).hex()}.png"
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], temp_filename)
                image.save(image_path)
                
            except Exception as e:
                return jsonify({'error': f'Invalid base64 image: {str(e)}'}), 400
        
        # Check for file upload
        elif 'image' in request.files:
            file = request.files['image']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            # Save uploaded file
            filename = f"upload_{os.urandom(8).hex()}_{file.filename}"
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)
        
        else:
            return jsonify({'error': 'No image provided'}), 400
        
        print(f"[API] Image saved to: {image_path}")
        
        # Determine which module to use
        module_type = determine_module(question)
        print(f"[API] Module selected: {module_type}")
        
        # Process with appropriate module
        if module_type == 'ocr':
            answer = process_with_ocr(image_path, question)
        else:
            answer = process_with_vqa(image_path, question)
        
        # Clean up temporary file
        try:
            if image_path and os.path.exists(image_path):
                os.remove(image_path)
        except:
            pass
        
        return jsonify({
            'success': True,
            'answer': answer,
            'module': module_type,
            'question': question
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/test', methods=['POST'])
def test_modules():
    """
    Test endpoint to check if VQA and OCR modules are available.
    
    Returns:
        JSON with module availability status
    """
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    
    vqa_available = False
    ocr_available = False
    
    try:
        from vqa.vqa_model import answer_question
        vqa_available = True
    except:
        pass
    
    try:
        from ocr.ocr_module import extract_text
        ocr_available = True
    except:
        pass
    
    return jsonify({
        'vqa_available': vqa_available,
        'ocr_available': ocr_available,
        'status': 'ready' if (vqa_available and ocr_available) else 'partial'
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
