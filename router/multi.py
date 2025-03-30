from fastapi import APIRouter, File, UploadFile
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from utils.intent_classifier import *
from utils.knowledge_retriever import get_disease_info
from utils.image_processing import preprocess_multiClass_image
from utils.model_loader import multi_model
from fastapi.templating import Jinja2Templates
from fastapi import Request
from PIL import Image
import numpy as np
import json

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/multiHtml", response_class=HTMLResponse)
async def get_multi_page(request: Request):
    return templates.TemplateResponse("multi.html", {"request": request})

@router.post("/multiPredict", response_class=JSONResponse)
async def predict_multi(image: UploadFile = File(...)):
    try:
        # Process and predict the uploaded image
        image = Image.open(image.file)
        processed_image = preprocess_multiClass_image(image)
        prediction = multi_model.predict(processed_image)
        predicted_class = np.argmax(prediction)

        # Map the predicted class to the corresponding disease
        class_map = {0: "Common Rust", 1: "Gray Leaf Spot", 2: "Healthy", 3: "Northern"}
        result = class_map.get(predicted_class, "Unknown")
        return {"result": result}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Prediction failed: {str(e)}"})
    
