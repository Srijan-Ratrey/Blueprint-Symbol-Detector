# Blueprint Symbol Detector

A FastAPI-based service for detecting electrical symbols in blueprint images.

## Features

- Detects three types of electrical symbols in blueprint images:
  - EV charger blocks (evse)
  - Electrical panelboards (panel)
  - GFI receptacles (gfi)
- Handles both PDF and image uploads (PNG/JPG)
- Provides visual output with bounding boxes
- Web interface for easy testing
- Docker support for deployment

## Project Structure

```
└── backend/
    ├── main.py            # FastAPI application
    ├── detector.py        # Symbol detection logic
    ├── config.py          # Configuration settings
    ├── requirements.txt   # Python dependencies
    ├── Dockerfile         # Docker container definition
    ├── static/            # Static files for web interface
    ├── uploads/           # Temporary storage for uploads
    └── output/            # Output files (visualizations)
```

## Getting Started

See the [backend README](backend/README.md) for detailed setup instructions.

### Quick Start

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run the API
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at http://localhost:8000

## API Endpoints

### POST /detect

Detects electrical symbols in a blueprint image or PDF.

- Input: PDF (single page) or PNG/JPG image
- Output: JSON with symbol detections and visualization URL

## License

MIT 