from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont
import io
import base64

app = Flask(__name__)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "API is running"}), 200

from flask import Flask, request, send_file
from flask_cors import CORS
from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/generate_image', methods=['POST'])
def generate_image():
    data = request.json
    
    # Print all fields in the dictionary
    print("Received Data:")
    for key, value in data.items():
        print(f"{key}: {value}")
    
    text = "\n".join([f"{key}: {value}" for key, value in data.items()])
    
    # Create an image
    img = Image.new('RGB', (400, 200), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 16)  # Try to load Arial font
    except:
        font = ImageFont.load_default()
    
    # Draw text on image line by line
    y_position = 10
    for line in text.split("\n"):
        draw.text((10, y_position), line, fill=(0, 0, 0), font=font)
        y_position += 20
    
    # Save to a byte buffer
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
