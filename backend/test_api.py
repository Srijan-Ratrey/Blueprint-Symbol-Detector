import os
import requests
import sys
import json
from PIL import Image
import io
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def test_api(file_path, api_url="http://localhost:8000/detect"):
    """
    Test the Blueprint Symbol Detector API
    
    Args:
        file_path: Path to a PDF or image file
        api_url: URL of the API endpoint
    """
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist")
        return
    
    print(f"Testing API with file: {file_path}")
    
    # Send the file to the API
    try:
        with open(file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(api_url, files=files)
    
        # Check the response
        if response.status_code == 200:
            result = response.json()
            
            # Print the detections
            print(f"API returned {len(result['detections'])} detections:")
            for i, detection in enumerate(result["detections"]):
                label = detection["label"]
                confidence = detection["confidence"]
                bbox = detection["bbox"]
                print(f"  {i+1}. {label}: {confidence:.2f}, bbox={bbox}")
            
            # Print the overlay image URL
            print(f"Overlay image URL: {result['image_url']}")
            
            # Try to display the overlay image
            try:
                response = requests.get(result['image_url'])
                img = Image.open(io.BytesIO(response.content))
                plt.figure(figsize=(10, 10))
                plt.imshow(img)
                plt.title("Detection Results")
                plt.axis('off')
                plt.show()
            except Exception as e:
                print(f"Could not display the overlay image: {e}")
                
            return result
        else:
            print(f"API Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Get file path from command line or use default
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        # Use a default test file if available
        if os.path.exists("../Trial Exercise/The Egyptian EV - Sample Data.pdf"):
            file_path = "../Trial Exercise/The Egyptian EV - Sample Data.pdf"
        else:
            print("Please provide a path to a PDF or image file")
            sys.exit(1)
    
    # Test the API
    test_api(file_path) 