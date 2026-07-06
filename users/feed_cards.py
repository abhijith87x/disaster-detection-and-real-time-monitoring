from fastapi import APIRouter
from database.database import cursor, mydb
from typing import Optional
from cache.redis_connection import r
from decimal import Decimal

import json

router = APIRouter()

cursor = mydb.cursor(dictionary=True)

@router.get("/feed/reports/latest")
async def get_latest_reports(page: int):
    LIMIT = 6
    OFFSET = (page - 1) * LIMIT
    
    reports = await r.get(f"feed:{OFFSET}:{LIMIT}")
  
    if reports is not None:
        print("reports from cache:", reports)
        return json.loads(reports)
    
    cursor.execute(
        "SELECT image_id, user_id, image_path, description, latitude, longitude, status FROM disaster_uploads ORDER BY created_at DESC LIMIT %s OFFSET %s",
        (LIMIT, OFFSET)
    )
    reports = cursor.fetchall()
    
    await r.set(f"feed:{OFFSET}:{LIMIT}",json.dumps(reports, default=float))
    return reports

@router.get("/feed/card/action")
async def user_action(
    currentUser : Optional[int] = None
):
    if currentUser:
        cursor.execute(
            "SELECT *  FROM reactions WHERE user_id=%s",(currentUser,)
        )
        useraction = cursor.fetchall()
        return useraction
    else:
        return None
