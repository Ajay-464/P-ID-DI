import cv2
import numpy as np
import os

def preprocess_image(image_path):
    """
    Applies a series of preprocessing steps to enhance P&ID image quality.
    - Converts to grayscale for uniform processing.
    - Applies adaptive thresholding to create a clean black & white (binary) image.
    - Removes small noise specks (morphological opening).
    """
    try:
        print(f"----------------//////// Preprocessing image: {os.path.basename(image_path)}...")
        img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)

        if img is None:
            print("Warning: Could not read image with OpenCV. Skipping preprocessing.")
            return image_path

        # 1. Denoising to reduce random noise from scans
        denoised_img = cv2.fastNlMeansDenoising(img, None, h=10, templateWindowSize=7, searchWindowSize=21)

        # 2. Adaptive Thresholding is excellent for handling uneven lighting
        binary_img = cv2.adaptiveThreshold(
            denoised_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 15, 4
        )

        # 3. Morphological Operations to clean up small specks and dots
        kernel = np.ones((1, 1), np.uint8)
        opening = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel, iterations=1)

        # Save the processed image to a temporary file
        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        processed_path = os.path.join(temp_dir, f"processed_{os.path.basename(image_path)}")
        
        cv2.imwrite(processed_path, opening)
        print(f"----------------//////// Image preprocessed and saved to {processed_path}")
        return processed_path

    except Exception as e:
        print(f" Error during image preprocessing: {e}. Using original image.")
        return image_path 

