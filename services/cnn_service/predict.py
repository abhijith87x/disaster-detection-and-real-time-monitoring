from fastapi import APIRouter, File, UploadFile
from screen_capture_model import predict_screen_capture
from disaster_prediction_model import predict_disaster
import time 
router = APIRouter()

@router.post("/detect/ScreenCapture")
async def detect_screen_captuture(file: UploadFile = File(...)):
    result = await predict_screen_capture(file)
    return result


@router.post("/detect/disaster")
async def detect_disaster(file: UploadFile = File(...)):
    # return {"status": "ok"}

    print("ENDPOINT START")
    
    start = time.perf_counter()
   
    result = await predict_disaster(file)
  
    print("PREDICT DONE:", time.perf_counter() - start)

    t_before_return = time.perf_counter()
    print(f"BEFORE RETURN: {t_before_return - start:.4f}s")
  
    return result
    