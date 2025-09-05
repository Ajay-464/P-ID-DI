import cv2
import os
import numpy as np
from PIL import Image

def draw_bounding_boxes(uploaded_file, detections, output_dir="temp_outputs"):
    """
    Draws bounding boxes from AI detections on the uploaded image.

    Parameters:
        uploaded_file (streamlit UploadedFile): The uploaded P&ID image.
        detections (dict): Extracted data with bounding_box info.
        output_dir (str): Temporary folder to save annotated image.

    Returns:
        str: Path to the saved annotated image.
    """
    # Convert uploaded file to OpenCV image
    image = Image.open(uploaded_file).convert("RGB")
    img_cv = np.array(image)
    img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)


    for category, items in detections.items():
        if isinstance(items, list):
            for item in items:
                if "bounding_box" in item and item["bounding_box"]:
                    try:
                        x1, y1, x2, y2 = map(int, item["bounding_box"])
                        label = item.get("label", category)

                        # Draw rectangle
                        cv2.rectangle(img_cv, (x1, y1), (x2, y2), (0, 255, 0), 2)

                        # Draw label text
                        cv2.putText(img_cv, label, (x1, max(y1 - 5, 15)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    except Exception as e:
                        print(f"Skipping invalid bbox in {category}: {e}")
    os.makedirs(output_dir, exist_ok=True)


    output_path = os.path.join(output_dir, "annotated_image.png")
    cv2.imwrite(output_path, img_cv)

    return output_path
