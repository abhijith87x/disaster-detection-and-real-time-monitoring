from fastapi import FastAPI
from .image_upload import router as upload_router

app =  FastAPI()

app.include_router(upload_router)