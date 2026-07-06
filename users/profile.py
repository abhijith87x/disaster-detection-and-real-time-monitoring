from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from httpx import request
from jwt.jwt_handler import get_current_user
from database.database import cursor

router = APIRouter()

@router.get("/profile")
async def get_profile(request : Request):
    token = request.cookies.get("access_token")
    if not token:
        return None
    else:
        try:
            payload =  await get_current_user(request)
            user_id = payload["user_id"]
            cursor.execute("SELECT id,email, name, profile_pic FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            return {
                "id": user[0],
                "email": user[1],
                "name": user[2],
                "profile_pic": user[3]
            }
        except HTTPException:
            return JSONResponse(status_code=401,content={ "detail": "Unauthorized"})
            
@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie(key="access_token")
    return response