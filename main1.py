import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.auth import router as auth_router
from users.image_route import router as image_router
from users.profile import router as profile_router
from users.feed_cards import router as feed_cards_router
from users.users_reactions import router as users_reactions_router
from starlette.middleware.sessions import SessionMiddleware
from config import client_secret
from fastapi.staticfiles import StaticFiles
from socket_app.socket_server import sio
import socketio

app = FastAPI()

socket_app = socketio.ASGIApp(sio, app)

#origins = [
    #"http://127.0.0.1:5500",
    #"http://localhost:5500"
#]

#app.add_middleware(
    #CORSMiddleware,
    #allow_origins = ["*"],
    #allow_credentials = True,
    #allow_methods = ["*"],
    #allow_headers = ["*"],
#)

app.add_middleware(SessionMiddleware, secret_key=client_secret)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/user_uploads", StaticFiles(directory="user_uploads"), name="uploads")

app.include_router(auth_router)
app.include_router(image_router)
app.include_router(profile_router)
app.include_router(feed_cards_router)
app.include_router(users_reactions_router)