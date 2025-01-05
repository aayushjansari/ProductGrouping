# Overview
A simple Flask Server that is designed to detect and group products based on brands.

# Features
1. Product detection: YOLO11n.pt pretrained on SKU110K
2. Feature Extraction: Employs ResNet18 to extract visual features of detected products
3. Product Grouping: Applies K-means clustering to group similar products based on visual and spatial features
4. Visualization: Generates output images with color-coded bounding boxes indicating product groups


# Dependencies
Flask==3.1.0
Flask-Cors==4.0.0
ultralytics==8.2.0
opencv-python==4.7.0.72
torch==2.0.1
torchvision==0.15.2
numpy==1.24.3
pandas==2.0.1
scikit-learn==1.2.2
scipy==1.10.1
Pillow==9.5.0
requests==2.30.0
pyyaml==6.0.1
Werkzeug==2.3.4

# **Installation**
# Create A Virtual Environment
python -m venv venv

# Install Dependencies
pip install -r requirements.txt


#  **Usage**
# Run flask Server
1. python main.py

2. goto: http://127.0.0.1:5000/

# Upload Image via API
1. Upload image
    URL: /upload
    Method: POST

    Example request:
    curl -X POST -F "image=@image.jpg" http://127.0.0.1:5000/upload
2. View results
    URL: /static/<filename>
    Method: GET

   Example request:
   curl -O http://127.0.0.1:5000/static/<filename>

# Configuration
1. Modify __init__.py to change upload/output directories
2. Adjust clustering parameters in grouping.py
3. Change detection model in detection.py

# **Contact**
Aayush Jansari
aayushjansari@gmail.com

