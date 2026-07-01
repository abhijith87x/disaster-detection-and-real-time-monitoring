import shutil
from fastapi import HTTPException, Request
from fastapi import APIRouter,Form,File,UploadFile
from ml.screen_capture_model import predict_screen_capture
from ml.disaster_model import predict_disaster
from jwt.jwt_handler import verify_token
from fastapi.templating import Jinja2Templates
from jinja2 import Template
from fastapi.responses import RedirectResponse, HTMLResponse
from jwt.jwt_handler import get_current_user
import uuid, os, requests
from database.database import cursor, mydb
from socket_app.feed_updates import card_update
from cache.redis_connection import r

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
        print("file received:", file.filename)
        return result
    except HTTPException:
        #return RedirectResponse(url="/login-page", status_code=303)
        raise HTTPException(status_code=401, detail="Unauthorized: Please log in to upload data")

async def get_location(lat, lon):
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"

        headers = {"User-Agent": "disaster-app/1.0"}

        response = requests.get(url, headers=headers, timeout=5)

        data = response.json()

        return data.get("display_name", "Unknown Location")

    except Exception as e:
        print("Location error:", e)
        return "Unknown Location"
   

@router.post("/demo")
async def demo(
    request : Request,
    File:UploadFile = File(...),
    latitude: str = Form(...),
    longitude: str = Form(...)
):
    try:
        user = await get_current_user(request)
        user_id = user["user_id"]
        print("User ID from token:", user_id)
        
        result = await predict_disaster(File)
        if result in ["Earthquake","Flood","Landslide","Wildfire"]:
            print("Disaster detected, saving file...")
            await File.seek(0)
            file = await File.read()
            extension = os.path.splitext(File.filename)[1]
            filename = f"{uuid.uuid4()}{extension}"
            file_path = f"user_uploads/{filename}"
            with open(file_path, "wb") as f:
                f.write(file)
            print(f"File saved to: {file_path}")
            location = await get_location(latitude, longitude)
            cursor.execute(
                "INSERT INTO disaster_uploads (user_id, image_path, disaster_type, latitude, longitude, description) VALUES ( %s, %s, %s, %s, %s, %s)", 
                ( user_id, 
                 file_path, 
                 result, 
                 latitude, 
                 longitude,
                 f"AI detected {result}-related visual patterns in the user uploaded image at {location}."
                )
            )
            last_row = cursor.lastrowid
            mydb.commit()
            keys = await r.keys("feed:*")
            if keys:
                await r.delete(*keys)
            print("Upload record saved to database")
            await card_update({
                "image_id" : last_row,
                "user_id" : user_id,
                "description" : f"AI detected {result}-related visual patterns in the user uploaded image at {location}.",
                "latitude" : latitude,
                "longitude" : longitude,
                "image_path" : file_path,
                "status" : "Unverified",   
            })
            print("websocket card report given    ",last_row)
            return "Disaster"
        else:
            return result
    except HTTPException:
        return RedirectResponse(url="/login-page")
    ##Possible flood detected in Kollam, Kerala, India (AI prediction).
    
    