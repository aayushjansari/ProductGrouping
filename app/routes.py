from flask import Blueprint, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
from .detection import detect_objects
from .grouping import group_products
from .visualization import visualize_groups

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def home():
    """Render the upload form by default."""
    return render_template('upload.html')

@main_blueprint.route('/upload', methods=['POST'])
def upload_image():
    # Check for uploaded image
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save uploaded file
    filename = secure_filename(file.filename)
    filepath = os.path.join('uploads', filename)
    file.save(filepath)

    # Step 1: Detect objects
    detections = detect_objects(filepath)
    if 'error' in detections:
        return jsonify(detections), 500

    # Step 2: Group products
    grouped_products = group_products(filepath, detections)
    if 'error' in grouped_products:
        return jsonify(grouped_products), 500

    # Step 3: Visualize groups
    visualized_image_path = visualize_groups(filepath, grouped_products['grouped_products'], output_name=filename)

    # Step 4: Return response to user
    response = grouped_products
    response['visualized_image'] = visualized_image_path

    return jsonify(response)


# to get the output image from API calls
@main_blueprint.route('/static/<filename>', methods=['GET'])
def get_visualized(filename):
    """Serve the visualized image."""
    try:
        return send_from_directory('static', filename)
    except FileNotFoundError:
        return jsonify({"error": f"Visualized file '{filename}' not found."}), 404
