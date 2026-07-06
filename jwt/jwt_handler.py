from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Template
from config import algorithm, expire_minutes, client_secret
from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import Request, HTTPException, status

templates = Jinja2Templates(directory="template")

async def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=int(expire_minutes))
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode, algorithm=algorithm, key=client_secret)
    return encoded_jwt

async def verify_token(token: str):
    try:
        payload = jwt.decode(token, key=client_secret, algorithms=[algorithm])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired or is invalid")
        
async def get_current_user(request : Request):
    token = request.cookies.get("access_token")
    try:
        payload = await verify_token(token)
        return payload
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired or is invalid")