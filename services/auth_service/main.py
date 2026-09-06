from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from auth import router as auth_router
from oauth_profile import router as profile_router
from config import client_secret

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=client_secret)

app.include_router(profile_router)
app.include_router(auth_router)

