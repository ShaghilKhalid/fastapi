from fastapi import FastAPI, File, UploadFile
from PIL import Image
import cv2
import numpy as np
import io
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Example function to check the car seat
def verify_seat(image: np.array) -> bool:
    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply GaussianBlur to reduce noise
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    
    # Perform edge detection
    edges = cv2.Canny(blurred_image, 50, 150)
    
    # Dummy check based on dimensions (you can define other checks)
    height, width = gray_image.shape[:2]
    min_width, max_width = 200, 500
    min_height, max_height = 300, 700
    
    if min_width <= width <= max_width and min_height <= height <= max_height:
        return True
    return False
@app.get("/getData")
def GETDATA():
    return {"message": "Welcome to the car seat verification API"}
@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))

    image = np.array(image)

    # Verify the car seat using custom logic
    is_valid_seat = verify_seat(image)

    # Return the result
    if is_valid_seat:
        return {"status": "success", "message": "Valid car seat"}
    else:
        return {"status": "error", "message": "Invalid car seat"}
