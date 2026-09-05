from fastapi import FastAPI
import socketio
from image_upload import router as upload_router
from socket_connection.socket_server import sio
from feed_cards import router as feed_router
from users_reactions import router as reactions_router

fastapi_app =  FastAPI()

fastapi_app.include_router(upload_router)
fastapi_app.include_router(feed_router)
fastapi_app.include_router(reactions_router)

app = socketio.ASGIApp(sio, fastapi_app)