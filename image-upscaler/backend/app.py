from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import cv2
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

UPLOAD_FOLDER = './uploads'
PROCESSED_FOLDER = './processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/upscale', methods=['POST'])
def upscale_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    # Save the uploaded image
    file = request.files['image']
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Read the image using OpenCV
    image = cv2.imread(filepath)
    if image is None:
        return jsonify({'error': 'Invalid image format'}), 400

    # Get original dimensions
    height, width = image.shape[:2]

    # Scale the image (2x upscale in this example)
    new_width = width * 2
    new_height = height * 2

    # Upscale using bilinear interpolation
    upscaled_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

    # Save the upscaled image
    processed_filepath = os.path.join(PROCESSED_FOLDER, f"upscaled_{filename}")
    cv2.imwrite(processed_filepath, upscaled_image)

    # Return the upscaled image to the client
    return send_file(processed_filepath, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
