"""
Assistive VQA - Main Entry Point
Runs the Flask backend API for the web application.
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.app import app

if __name__ == '__main__':
    print("=" * 60)
    print("Assistive VQA System")
    print("=" * 60)
    print("\nBackend API running on: http://localhost:5001")
    print("Frontend (Next.js): Run 'npm run dev' in ui-webapp/ directory")
    print("\nAPI Endpoints:")
    print("  - GET  /api/health - Health check")
    print("  - POST /api/query  - Process image + question")
    print("  - POST /api/test   - Test module availability")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5001)
