from fastapi import APIRouter
from database.database import cursor, mydb
from typing import Optional
router = APIRouter()

cursor = mydb.cursor(dictionary=True)

@router.get("/feed/reports/latest")
async def get_latest_reports(page: int = 1):
    LIMIT = 6
    OFFSET = (page - 1) * LIMIT
    cursor.execute(
        "SELECT image_id, user_id, image_path, description FROM disaster_uploads ORDER BY created_at DESC LIMIT %s OFFSET %s",
        (LIMIT, OFFSET)
    )
    reports = cursor.fetchall()
    return reports

@router.get("/feed/card/action")
async def user_action(
    currentUser : Optional[int] = None
):
    if currentUser:
        print('currentttttt',currentUser)
        cursor.execute(
            "SELECT *  FROM reactions WHERE user_id=%s",(currentUser,)
        )
        useraction = cursor.fetchall()
        print(useraction)
        return useraction
    else:
        return None
