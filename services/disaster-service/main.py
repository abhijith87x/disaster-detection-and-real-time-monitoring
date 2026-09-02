from fastapi import FastAPI
import socketio
from image_upload import router as upload_router
from socket_connection.socket_server import sio

fastapi_app =  FastAPI()

fastapi_app.include_router(upload_router)

app = socketio.ASGIApp(sio, fastapi_app)