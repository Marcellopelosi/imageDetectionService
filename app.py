from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from ultralytics import YOLO
from PIL import Image, ImageDraw
import io
import base64

app = Flask(__name__)
CORS(app)

# Load YOLO model
model = YOLO('yolov8n.pt')  # Adjust model as needed

@app.route('/api/detect', methods=['POST'])
def detect_objects():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']
    image = Image.open(image_file.stream).convert('RGB')
    results = model(image)

    # Draw bounding boxes on the image
    draw = ImageDraw.Draw(image)
    detected_objects = []
    colors = ["red", "blue", "green", "yellow", "pink"]
    cls = results[0].boxes.cls
    for i in range(len(cls)):
        x1, y1, x2, y2 = [float(i) for i in list(results[0].boxes.xyxy[i])]
        confidence = float(results[0].boxes.conf[i])
        detected_objects.append({
            "class": results[0].names[int(cls[i])],
            "confidence": confidence,
            "color": colors[i],
            "bbox": [x1, y1, x2, y2],
        })
        # Draw the bounding box
        draw.rectangle([x1, y1, x2, y2], outline=colors[i], width=5)

    # Convert image to base64
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

    # Return detected objects and image
    return jsonify({"detected_objects": detected_objects, "image": img_str}), 200

if __name__ == '__main__':
    app.run(debug=True)
