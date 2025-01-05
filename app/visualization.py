import cv2
import numpy as np
import os

def visualize_groups(image_path, detections, output_folder="static", output_name="visualized_output.jpg"):
    # Load the image
    image = cv2.imread(image_path)

    # Assign colors to each group
    colors = {}
    for detection in detections:
        group_id = detection['group_id']
        if group_id not in colors:
            colors[group_id] = tuple(np.random.randint(0, 255, 3).tolist())

    # Draw bounding boxes and group labels same as the reference image in the assignment
    for detection in detections:
        x1, y1, x2, y2 = detection['coordinates']
        group_id = detection['group_id']
        color = colors[group_id]
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

    # Save the visualized image
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, f"visualized_{output_name}")
    cv2.imwrite(output_path, image)

    return output_path
