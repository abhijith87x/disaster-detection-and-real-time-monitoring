from fastapi import Request
from fastapi import FastAPI,Form,File,UploadFile,HTTPException,status
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
import io
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
from fastapi.responses import RedirectResponse,HTMLResponse
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import mysql.connector
from jinja2 import Template

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "8714176972",
    database = "disaster_db"
)

cursor = mydb.cursor()
app = FastAPI()

origins = [
    "http://127.0.0.1:5500"
    "http://localhost:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

class DBModel(BaseModel):
    name : str
    email : str

templates = Jinja2Templates(directory="template")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index1.html",{"request": request})
 
# FOR THE DEMO
@app.post("/demo")
async def demo(
    File:UploadFile = File(...),
    latitude: str = Form(...),
    longitude: str = Form(...)
):
   ## model = tf.keras.models.load_model("Disaster_detector.keras")
    model = load_model("Disaster_detector.keras", compile=False)
    image_bytes = await File.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((128,128))
    image_array = np.array(image)
    image_array = image_array/255.0
    Final_image = np.expand_dims(image_array,axis=0)
    prediction = model.predict(Final_image)[0][0]
    if prediction > 0.5:
        return{"Non_Disaster"}
    else:
        return{"Disaster"}
    
@app.post("/uploaddata")
async def upload(
    latitude: str = Form(...),
    longitude: str = Form(...),
    file:UploadFile = File(...),
    date: str = Form(...) 
):  
    print(f"Received:  {date}, {latitude}, {longitude}, {file}")
    #return{"message":"hloo"}
    #return {"message": "Data received successfully"}
    if file.content_type  in  ["img/jpeg","img/png"]:
        return{"success":"ok"}
    model = tf.keras.models.load_model("screen_image_detector.keras")
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((128,128))
    image_array = np.array(image)
    image_array = image_array/255.0
    Final_image = np.expand_dims(image_array,axis=0)
    prediction = model.predict(Final_image)[0][0]
    if prediction > 0.5:
        return{"Screen_captured_image"}
    else:
        model = tf.keras.models.load_model("Disaster_detector.keras")
        prediction = model.predict(Final_image)[0][0]
        if prediction > 0.5:
            return{"Non_Disaster"}
        else:
            return{"Disaster"}

app.add_middleware(SessionMiddleware, secret_key="secret")
oauth = OAuth()
oauth.register(
    name="google",
    client_id="263416368181-78703jncig7jcdr1b8749f50lq7udbbh.apps.googleusercontent.com",
    client_secret="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",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile"
    }
)

@app.get("/login")
async def login( request : Request):
   return await oauth.google.authorize_redirect(request, redirect_uri="http://localhost:8000/auth/google/callback") 

@app.get("/auth/google/callback")
async def google_callback(request : Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get("userinfo") or {}
        email = user_info.get("email")
        name = user_info.get("name")
        google_id = user_info.get("sub")
        profile = user_info.get("picture")
       
        cursor.execute(
            "SELECT * FROM users WHERE email = %s",(email,)
        )
        existing_user = cursor.fetchone()
        if not existing_user:
            cursor.execute(
                "INSERT INTO users (email, name, google_id, profile_pic) VALUES (%s, %s, %s, %s)",
                (email, name, google_id, profile)
            )
            mydb.commit()
            print("New user added to database")
        else:
            print("User already exists in database")
        return RedirectResponse(url="/")
        
    except Exception as e:
        import traceback
        print("error",traceback.format_exc())
        return{"error": str(e)}