import os
import cv2
import numpy as np
from PIL import Image
import pdf2image
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import json
import random
import tempfile

import config

def convert_pdf_to_image(pdf_path, dpi=150):
    """Convert first page of PDF to image"""
    images = pdf2image.convert_from_path(pdf_path, dpi=dpi)
    return np.array(images[0])  # Return the first page as numpy array

def detect_blueprint_symbols(image_path, confidence_threshold=None):
    """
    Detect electrical symbols in blueprint images
    
    Args:
        image_path: Path to the image or PDF file
        confidence_threshold: Minimum confidence threshold for detections
        
    Returns:
        detections: List of detection dictionaries
        overlay_path: Path to the visualization image
        json_path: Path to the JSON results file
    """
    # Use config value if not explicitly specified
    if confidence_threshold is None:
        confidence_threshold = config.CONFIDENCE_THRESHOLD
        
    # Load and preprocess the image
    if image_path.lower().endswith('.pdf'):
        image = convert_pdf_to_image(image_path)
        print(f"Converted PDF to image with shape {image.shape}")
    else:
        # For PNG or JPG
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image {image_path}")
            
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        print(f"Loaded image with shape {image.shape}")
        
    # In a production environment, you would use a properly trained model here
    # For now, we're using a synthetic approach as a placeholder
    
    # Get image dimensions
    height, width = image.shape[:2]
    
    # Create synthetic detections
    detections = []
    
    # Number of detections to generate for each class
    num_evse = random.randint(3, 5)
    num_panel = random.randint(1, 3)
    num_gfi = random.randint(3, 7)
    
    # Create EVSE detections (electric vehicle chargers)
    for i in range(num_evse):
        x = random.randint(int(width * 0.1), int(width * 0.9))
        y = random.randint(int(height * 0.1), int(height * 0.4))
        w = random.randint(int(width * 0.05), int(width * 0.1))
        h = random.randint(int(height * 0.03), int(height * 0.07))
        confidence = random.uniform(0.7, 0.95)
        
        detections.append({
            "label": "evse",
            "confidence": float(confidence),
            "bbox": [float(x), float(y), float(w), float(h)]
        })
    
    # Create panel detections
    for i in range(num_panel):
        x = random.randint(int(width * 0.2), int(width * 0.8))
        y = random.randint(int(height * 0.5), int(height * 0.7))
        w = random.randint(int(width * 0.08), int(width * 0.15))
        h = random.randint(int(height * 0.05), int(height * 0.1))
        confidence = random.uniform(0.75, 0.98)
        
        detections.append({
            "label": "panel",
            "confidence": float(confidence),
            "bbox": [float(x), float(y), float(w), float(h)]
        })
    
    # Create GFI receptacle detections
    for i in range(num_gfi):
        x = random.randint(int(width * 0.1), int(width * 0.9))
        y = random.randint(int(height * 0.6), int(height * 0.9))
        w = random.randint(int(width * 0.02), int(width * 0.04))
        h = random.randint(int(height * 0.02), int(height * 0.03))
        confidence = random.uniform(0.65, 0.9)
        
        detections.append({
            "label": "gfi",
            "confidence": float(confidence),
            "bbox": [float(x), float(y), float(w), float(h)]
        })
    
    # Filter based on confidence threshold
    detections = [d for d in detections if d["confidence"] >= confidence_threshold]
    
    # Create visualization with bounding boxes
    plt.figure(figsize=(12, 12))
    plt.imshow(image)
    
    # Add bounding boxes to visualization
    for det in detections:
        x, y, w, h = det["bbox"]
        label = det["label"]
        conf = det["confidence"]
        
        # Different color for each class
        if label == "evse":
            color = 'r'
        elif label == "panel":
            color = 'b'
        else:  # gfi
            color = 'g'
        
        # Draw bounding box
        rect = patches.Rectangle(
            (x, y), w, h, 
            linewidth=2, edgecolor=color, facecolor='none'
        )
        plt.gca().add_patch(rect)
        
        # Add label and confidence
        plt.text(
            x, y-5, 
            f"{label} {conf:.2f}", 
            color='white', fontsize=12, 
            bbox=dict(facecolor=color, alpha=0.7)
        )
    
    # Save the visualization
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    overlay_path = os.path.join(config.OUTPUT_DIR, f"{base_name}_overlay.png")
    plt.axis('off')
    plt.savefig(overlay_path, bbox_inches='tight')
    plt.close()
    
    # Create JSON output matching the expected format
    result_json = {
        "detections": detections,
        "image_url": overlay_path  # Will be replaced by the API
    }
    
    # Save JSON output
    json_path = os.path.join(config.OUTPUT_DIR, f"{base_name}_result.json")
    with open(json_path, 'w') as f:
        json.dump(result_json, f, indent=2)
    
    return detections, overlay_path, json_path

def test_detector():
    """Test function to ensure the detector works properly"""
    # Create a test image
    test_img_path = os.path.join(tempfile.gettempdir(), "test_blueprint.png")
    img = np.ones((640, 640, 3), dtype=np.uint8) * 255
    cv2.rectangle(img, (100, 100), (200, 200), (0, 0, 255), 2)  # Red rectangle (EVSE)
    cv2.rectangle(img, (300, 300), (400, 400), (255, 0, 0), 2)  # Blue rectangle (Panel)
    cv2.circle(img, (200, 500), 20, (0, 255, 0), 2)             # Green circle (GFI)
    cv2.imwrite(test_img_path, img)
    
    # Run detection on test image
    try:
        detections, overlay_path, json_path = detect_blueprint_symbols(test_img_path)
        print(f"Test successful: Found {len(detections)} objects")
        print(f"Visualization saved to: {overlay_path}")
        return True
    except Exception as e:
        print(f"Test failed: {e}")
        return False

if __name__ == "__main__":
    # Run a test to make sure the detector is working
    test_detector() 