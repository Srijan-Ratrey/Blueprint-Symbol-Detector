from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import shutil
from datetime import datetime
import uuid

from detector import detect_blueprint_symbols
import config

# Create FastAPI app
app = FastAPI(
    title="Blueprint Symbol Detector API",
    description="API for detecting electrical symbols in blueprint images",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
app.mount("/static", StaticFiles(directory=config.STATIC_DIR), name="static")

@app.get("/")
async def root():
    """Redirect to the HTML interface"""
    return RedirectResponse(url="/static/index.html")

@app.get("/api")
async def api_info():
    """API info endpoint"""
    return {
        "message": "Blueprint Symbol Detector API",
        "version": "1.0.0",
        "endpoints": {
            "/detect": "POST - Detect symbols in blueprint image/PDF",
            "/static/index.html": "GET - Web interface for testing the API"
        }
    }

@app.post("/detect")
async def detect_symbols(file: UploadFile = File(...)):
    """
    Detect electrical symbols in a blueprint image/PDF
    
    - **file**: PDF (single page) or PNG/JPG image of the page
    
    Returns:
        JSON with detections and image overlay URL
    """
    # Check file size (10MB limit)
    file_size = 0
    file_data = await file.read()
    file_size = len(file_data)
    
    if file_size > config.MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Maximum size is 10MB.")
    
    # Check file type
    content_type = file.content_type
    if not (content_type.startswith('application/pdf') or
            content_type.startswith('image/jpeg') or
            content_type.startswith('image/png')):
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Only PDF, JPG, and PNG are supported."
        )
    
    # Create a unique filename
    ext = os.path.splitext(file.filename)[1].lower()
    if not ext:
        ext = '.pdf' if content_type.startswith('application/pdf') else '.png'
    
    unique_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{unique_id}{ext}"
    file_path = os.path.join(config.UPLOAD_DIR, filename)
    
    # Save uploaded file
    with open(file_path, "wb") as f:
        f.write(file_data)
    
    try:
        # Run detection
        detections, overlay_path, _ = detect_blueprint_symbols(
            file_path, 
            confidence_threshold=config.CONFIDENCE_THRESHOLD
        )
        
        # Create a URL for the overlay image
        overlay_filename = os.path.basename(overlay_path)
        
        # Copy the overlay image to the static directory
        static_overlay_path = os.path.join(config.STATIC_DIR, overlay_filename)
        shutil.copy(overlay_path, static_overlay_path)
        
        # Create the public URL to serve the image
        image_url = f"{config.API_BASE_URL}/static/{overlay_filename}"
        
        # Return the results
        return JSONResponse({
            "detections": detections,
            "image_url": image_url
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    
    finally:
        # Clean up the uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == "__main__":
    uvicorn.run("main:app", host=config.HOST, port=config.PORT, reload=True) 