# Blueprint Symbol Detector API

This is a FastAPI service that detects electrical symbols in blueprint images and returns their positions.

## Supported Symbols

| Symbol | API label |
| --- | --- |
| EV charger block | `evse` |
| Electrical panelboard | `panel` |
| GFI receptacle | `gfi` |

## Setup and Running

### Prerequisites

- Python 3.8 or higher
- poppler-utils (for PDF processing)

### Installation

1. Install poppler-utils for PDF processing:

```bash
# For macOS
brew install poppler

# For Ubuntu/Debian
sudo apt-get install poppler-utils

# For Windows
# Download and install poppler from http://blog.alivate.com.au/poppler-windows/
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

### Running the API

From the backend directory:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Or using Python:

```bash
python main.py
```

The API will be available at http://localhost:8000

## API Endpoints

### POST /detect

Detects electrical symbols in a blueprint image or PDF.

**Input:**
- Form field name: `file`
- Accepted formats: PDF (single page), PNG, or JPG
- Max size: 10 MB

**Output (JSON):**
```json
{
  "detections": [
    {
      "label": "evse",
      "confidence": 0.91,
      "bbox": [x, y, width, height]
    },
    {
      "label": "panel",
      "confidence": 0.88,
      "bbox": [x, y, width, height]
    }
    // ... more boxes ...
  ],
  "image_url": "http://localhost:8000/static/overlay.png"
}
```

## Using the API

### cURL Example

```bash
curl -X POST "http://localhost:8000/detect" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/blueprint.pdf"
```

### Python Example

```python
import requests

url = "http://localhost:8000/detect"
files = {"file": open("path/to/blueprint.pdf", "rb")}

response = requests.post(url, files=files)
result = response.json()

# Access detections
for detection in result["detections"]:
    print(f"{detection['label']}: confidence={detection['confidence']}, bbox={detection['bbox']}")

# Display or save the overlay image
print(f"Overlay image URL: {result['image_url']}")
```

## Using with Docker

Build the Docker image:

```bash
# From the root of the project
docker build -f backend/Dockerfile -t blueprint-detector-api .
```

Run the container:

```bash
docker run -p 8000:8000 blueprint-detector-api
```

The API will be available at http://localhost:8000 