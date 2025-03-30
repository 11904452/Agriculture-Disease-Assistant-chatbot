from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse
from utils.image_processing import preprocess_binary_image
from utils.model_loader import binary_model
from fastapi.templating import Jinja2Templates
from fastapi import Request
from PIL import Image
import numpy as np

router = APIRouter()
templates = Jinja2Templates(directory="./templates")

@router.get("/", response_class=HTMLResponse)
async def get_binary_page(request: Request):
    return templates.TemplateResponse("binary.html", {"request": request})

@router.post("/binaryPredict", response_class=JSONResponse)
async def predict_binary(image: UploadFile = File(...)):
    image = Image.open(image.file)
    processed_image = preprocess_binary_image(image)
    prediction = binary_model.predict(processed_image)
    predicted_class = np.argmax(prediction)
    
    result = "Healthy" if predicted_class == 2 else "Diseased"
    return {"result": result}
