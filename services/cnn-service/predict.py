from fastapi import APIRouter, File, UploadFile
from screen_capture_model import get_screen_model
from disaster_prediction_model import predict_disaster

router = APIRouter()

@router.post("/detect/ScreenCapture")
async def detect_screen_captuture(file: UploadFile = File(...)):
    result = await get_screen_model(file)
    return result

@router.post("/detect/disaster")
async def detect_disaster(file: UploadFile = File(...)):
    result = await predict_disaster(file)
    return result
    