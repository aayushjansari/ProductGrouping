import cv2
from ultralytics import YOLO

def detect_objects(image_path):
    try:
        model = YOLO('kaggle_best.pt') 
        results = model(image_path)

        detections = []
        for box in results[0].boxes.data:
            x1, y1, x2, y2, conf, cls = box.cpu().numpy() # convert box.cpu tensor to numpy arrat
            detections.append({
                "coordinates": [int(x1), int(y1), int(x2), int(y2)],
                "confidence": float(conf),
                "class_id": int(cls)
            })
        
        return {"detections": detections}
    except Exception as e:
        return {"error": str(e)}


