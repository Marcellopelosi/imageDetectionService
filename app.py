from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from ultralytics import YOLO
from PIL import Image, ImageDraw
import io
import base64

app = Flask(__name__)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "API is running"}), 200

@app.route('/process-text', methods=['POST'])
def process_text():
    # Get the input JSON data
    data = request.get_json()
    
    # Check if 'text' is provided in the request
    if 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    input_text = data['text']
    
    # Example processing: Reverse the input text
    output_text = input_text[::-1]
    
    # Return the processed text as JSON
    return jsonify({'input': input_text, 'output': output_text})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
