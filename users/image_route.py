from fastapi import HTTPException, Request
from fastapi import APIRouter,Form,File,UploadFile
from ml.screen_capture_model import predict_screen_capture
from ml.disaster_model import predict_disaster
from jwt.jwt_handler import verify_token
from fastapi.templating import Jinja2Templates
from jinja2 import Template
from fastapi.responses import RedirectResponse, HTMLResponse
from jwt.jwt_handler import get_current_user
router = APIRouter()

templates = Jinja2Templates(directory="template")

@router.get("/upload-form", response_class=HTMLResponse)
async def get_upload_form(request : Request):
    print("Request cookies:", request.cookies)
    try:
        token = request.cookies.get("access_token")
        print("Retrieved token:", token)
        if token is None:
            return RedirectResponse(url="/login-page")
        user = await get_current_user(request)
        return templates.TemplateResponse("demo.html", {"request": request})
    except HTTPException:
        return RedirectResponse(url="/login-page")

@router.get("/input-camera", response_class=HTMLResponse)
async def input_camera(request : Request):
    try:
        token = request.cookies.get("access_token")
        print("Retrieved token:", token)
        if token is None:
            return RedirectResponse(url="/login-page")
        user = await get_current_user(request)
        return templates.TemplateResponse("for_camera.html", {"request": request})
    except HTTPException:
        return RedirectResponse(url="/login-page", status_code=303)
        #raise HTTPException(status_code=401, detail="Unauthorized: Please log in to access the camera input form")
@router.post("/upload-data")
async def upload(
    request : Request,
    latitude: str = Form(...),
    longitude: str = Form(...),
    file:UploadFile = File(...),
    date: str = Form(...) 
):
    try:
        token = request.cookies.get("access_token")
        print("Retrieved token:", token)
        if token is None:
            return RedirectResponse(url="/login-page")
        user = await get_current_user(request)
        
        ######hereeee
        
        result = await predict_screen_capture(file)
        print(result)
        return result
    except HTTPException:
        #return RedirectResponse(url="/login-page", status_code=303)
        raise HTTPException(status_code=401, detail="Unauthorized: Please log in to upload data")
        
   

@router.post("/demo")
async def demo(
    request : Request,
    File:UploadFile = File(...),
    latitude: str = Form(...),
    longitude: str = Form(...)
):
    try:
        user = await get_current_user(request)
        
        ######hereeee
        
        result = await predict_disaster(File)
        return result
    except HTTPException:
        return RedirectResponse(url="/login-page")
    