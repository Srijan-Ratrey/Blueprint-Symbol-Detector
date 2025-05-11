#!/bin/bash
set -e

echo "=== Blueprint Symbol Detector API ==="

# Check if requirements are installed
if ! pip list | grep -q "fastapi"; then
    echo "Installing required packages..."
    pip install -r requirements.txt
fi

# Check if poppler-utils is installed (needed for PDF processing)
if ! command -v pdftoppm &> /dev/null; then
    echo "Warning: pdftoppm (poppler-utils) is not installed."
    echo "PDF processing may not work correctly."
    echo "Please install poppler-utils:"
    echo "  - macOS: brew install poppler"
    echo "  - Ubuntu/Debian: sudo apt-get install poppler-utils"
    echo "  - Windows: Download from http://blog.alivate.com.au/poppler-windows/"
fi

# Create necessary directories
mkdir -p uploads output static

# Run the FastAPI server
echo "Starting Blueprint Symbol Detector API on port 8000..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload 