import cv2
import torch
from torchvision import models, transforms
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np

# Load feature extractor
feature_extractor = models.resnet18(pretrained=True)
feature_extractor = torch.nn.Sequential(*(list(feature_extractor.children())[:-1]))
feature_extractor.eval()

def preprocess_image(image):
    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    return transform(image).unsqueeze(0)

def analyze_shelf_arrangement(detections, image_shape):
    """
    Without shelf analysis, the k means clustering was creating different groups for the same products on the same shelf
    Add shelf-level features to detections for enhanced grouping.
    This includes spatial analysis, such as proximity and row-column positioning
    """
    shelf_features = []
    image_height, image_width = image_shape[:2]

    for detection in detections['detections']:
        x1, y1, x2, y2 = detection['coordinates']
        center_x = (x1 + x2) / 2 / image_width
        center_y = (y1 + y2) / 2 / image_height
        width = (x2 - x1) / image_width
        height = (y2 - y1) / image_height
        shelf_features.append([center_x, center_y, width, height])

    return np.array(shelf_features)

def group_products(image_path, detections, n_clusters=5):
    try:
        image = cv2.imread(image_path)
        features = []

        for detection in detections['detections']:
            x1, y1, x2, y2 = detection['coordinates']
            cropped_image = image[y1:y2, x1:x2]
            cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)
            input_tensor = preprocess_image(cropped_image)
            with torch.no_grad():
                feature_vector = feature_extractor(input_tensor).squeeze().numpy()
            features.append(feature_vector)

        # Add shelf-level features for enhanced grouping
        shelf_features = analyze_shelf_arrangement(detections, image.shape)
        features = np.hstack((features, shelf_features))

        # Dimensionality reduction
        pca = PCA(n_components=min(50, min(features.shape[0], features.shape[1])))
        features_reduced = pca.fit_transform(features)

        # Clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        group_ids = kmeans.fit_predict(features_reduced)

        for i, detection in enumerate(detections['detections']):
            detection['group_id'] = int(group_ids[i])
            
        return {"grouped_products": detections['detections']}
    
    except Exception as e:
        return {"error": str(e)}
