from fastapi.responses import RedirectResponse
from config import client_id, client_secret
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import Request, Response
from fastapi import APIRouter
from database.database import cursor, mydb
from fastapi.templating import Jinja2Templates
from jinja2 import Template
from config import algorithm, expire_minutes
from datetime import datetime, timedelta
import jwt
from jwt.jwt_handler import create_access_token, verify_token

router = APIRouter()

oauth = OAuth()

oauth.register(
    name="google",
    client_id=client_id,
    client_secret=client_secret,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile"
    }
)

templates = Jinja2Templates(directory="template")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index1.html",{"request": request})

@router.get("/login-page", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/login")
async def login( request : Request):
   return await oauth.google.authorize_redirect(request, redirect_uri="https://disaster-watch.duckdns.org/auth/google/callback") 

@router.get("/auth/google/callback")
async def google_callback(request : Request):
    try:
        print("Callback URL:")
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get("userinfo") or {}
        email = user_info.get("email")
        print("Email:", email)
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
            cursor.execute(
                "SELECT id FROM users WHERE email = %s",(email,)
            )
            existing_user = cursor.fetchone()
        
        jwt_token = await create_access_token(data={"sub": email,"user_id": existing_user[0] })
        response = RedirectResponse(url="/")
        
        response.set_cookie(
            key="access_token",
            value=jwt_token,
            httponly=True,
            samesite="lax",
            secure=False,
            path="/"
        )
        return response
        
    except Exception as e:
        import traceback
        return{"error": str(e)}