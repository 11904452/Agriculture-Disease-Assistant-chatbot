import base64
import numpy as np
import cv2 as cv
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from DisplayDisease import DisplayDisease
from fastapi.templating import Jinja2Templates
from fastapi import Request

router = APIRouter()
templates = Jinja2Templates(directory="templates")
dd = DisplayDisease()

@router.get("/", response_class=HTMLResponse)
async def get_segment_page(request: Request):
    return templates.TemplateResponse("segment.html", {"request": request})

@router.post("/segmentPredict", response_class=JSONResponse)
async def segment_image(image: UploadFile = File(...)):
    img = cv.imdecode(np.frombuffer(image.file.read(), np.uint8), cv.IMREAD_UNCHANGED)
    dd.readImage(img)
    dd.removeNoise()
    dd.displayDisease()

    img_str = cv.imencode('.jpg', dd.getImage())[1].tobytes()
    img_base64 = base64.b64encode(img_str).decode()
    return {"image": img_base64}
