from fastapi import APIRouter
from database.database import cursor,mydb
from socket_app.feed_updates import card_del, status_update, update_description
from users.image_route import get_location
from cache.redis_connection import r
router = APIRouter()
cursor = mydb.cursor(dictionary = True)

@router.post("/user/like/update")
async def like_update(
    current_user : int,
    card_id : int,
    like : bool
):
    cursor.execute(
        "SELECT user_id, card_id, reaction, reported FROM reactions WHERE user_id=%s AND card_id=%s",(current_user,card_id)
    )
    card_info = cursor.fetchone()   
    user_id = card_info["user_id"] if card_info else None
    card_ID = card_info["card_id"] if card_info else None
    reported = card_info["reported"] if card_info else None
    if like:
        if user_id and card_ID:
            cursor.execute(
                "UPDATE reactions SET reaction = %s WHERE user_id=%s AND card_id=%s",("LIKE", current_user, card_id)
            )
            cursor.execute(
                  "UPDATE reactions SET suggested_type = %s WHERE user_id = %s AND card_id = %s",(None, current_user, card_id)
            )
            mydb.commit()
        else:
            cursor.execute(
                "INSERT INTO reactions (user_id, card_id, reaction) VALUES (%s, %s, %s)",(current_user ,card_id, "LIKE")
            )
            mydb.commit()
        
        cursor.execute(
            "SELECT COUNT(*) as like_count FROM reactions WHERE card_id=%s AND reaction='LIKE'",(card_id,)
        )
        like_count = cursor.fetchone()["like_count"]
           
        if like_count == 1:
            cursor.execute(
                "UPDATE disaster_uploads SET status=%s WHERE image_id=%s",('Verified',card_id)
            )
            mydb.commit()
            keys = await r.keys("feed:*")
            if keys:
                await r.delete(*keys)
            status = {
                "status" : "Verified",
                "card_id" : card_id
            }
            await status_update(status)
            
    else:
        if not reported:
            cursor.execute(
                "DELETE FROM reactions WHERE user_id=%s AND card_id=%s",(current_user, card_id)
            )
            mydb.commit()
        else:
            cursor.execute(
                "UPDATE reactions SET reaction = %s WHERE user_id=%s AND card_id=%s",(None, current_user, card_id)
            )
            mydb.commit() 
        
        cursor.execute(
            "SELECT COUNT(*) as like_count FROM reactions WHERE card_id=%s AND reaction='LIKE'",(card_id,)
        )
        like_count = cursor.fetchone()["like_count"]
        
        ##if like_count == 1:
            #cursor.execute(
                #"UPDATE disaster_uploads SET status=%s WHERE image_id=%s",('Verified', card_id)
            #)
            #mydb.commit()
        if like_count < 1:
            cursor.execute(
                "UPDATE disaster_uploads SET status=%s WHERE image_id=%s",('Unverified', card_id)
            )
            mydb.commit() 
            keys = await r.keys("feed:*")
            if keys:
                await r.delete(*keys)
            status = {
                "status" : "Unverified",
                "card_id" : card_id
            }
            await status_update(status)
               
@router.post("/user/dislike/update") 
async def dislike_update(
    current_user : int,
    card_id : int,
    dislike : bool,
    type : str | None = None
):
    cursor.execute(
        "SELECT user_id, card_id, reaction, reported FROM reactions WHERE user_id=%s AND card_id=%s",(current_user,card_id)
    )
    card_info = cursor.fetchone()
    user_id = card_info["user_id"] if card_info else None
    card_ID = card_info["card_id"] if card_info else None
    reported = card_info["reported"] if card_info else None
    
    if dislike:
        if user_id and card_ID:
            cursor.execute(
                "UPDATE reactions SET reaction = %s, suggested_type=%s WHERE user_id=%s AND card_id=%s",("DISLIKE",type, current_user, card_id)
            )
            mydb.commit()
        else:
            cursor.execute(
                "INSERT INTO reactions (user_id, card_id, reaction, suggested_type) VALUES (%s, %s, %s, %s)",(current_user ,card_id, "DISLIKE", type)
            )
            mydb.commit()
            
        cursor.execute(
            "SELECT COUNT(*) AS type_count FROM reactions WHERE card_id = %s AND reaction = %s GROUP BY suggested_type ORDER BY type_count DESC LIMIT 1",
            (card_id, 'DISLIKE')
        )
        type_count = cursor.fetchone()["type_count"]
        if type_count == 1:
            cursor.execute(
                "SELECT latitude, longitude FROM disaster_uploads WHERE image_id=%s",(card_id,)
            )
            location = cursor.fetchone()
            
            latitude, longitude = location["latitude"], location["longitude"]
            location = await get_location(latitude, longitude)
            description = f"AI detected {type}-related visual patterns in the user uploaded image at {location}."
            cursor.execute(
                "UPDATE disaster_uploads SET description = %s, disaster_type = %s WHERE image_id=%s",(description, type, card_id)
            )
            print("looking card",card_id)
            mydb.commit()
            keys = await r.keys("feed:*")
            if keys:
                await r.delete(*keys)
            data = {
                "description" : description,
                "card_id" : card_id
            }
            await update_description(data)
            
            cursor.execute(
                "SELECT COUNT(*) as like_count FROM reactions WHERE card_id=%s AND reaction='LIKE'",(card_id,)
            )
            like_count = cursor.fetchone()["like_count"]
            if like_count < 1:
                cursor.execute(
                    "UPDATE disaster_uploads SET status=%s WHERE image_id=%s",('Unverified',card_id)
                )
                mydb.commit()
                keys = await r.keys("feed:*")
                if keys:
                    await r.delete(*keys)
                status = {
                    "status" : "Unverified",
                    "card_id" : card_id
                }
                await status_update(status)
            
    else:
        if not reported:
            cursor.execute(
                "DELETE FROM reactions WHERE user_id=%s AND card_id=%s",(current_user, card_id)
            )
            mydb.commit()
        else:
            cursor.execute(
                "UPDATE reactions SET reaction = %s, suggested_type=%s WHERE user_id=%s AND card_id=%s",(None, None, current_user, card_id)
            )
            mydb.commit()
        
@router.post("/user/report/update") 
async def report_update(
    current_user : int,
    card_id : int,
    report : bool
):
    cursor.execute(
        "SELECT user_id, card_id, reaction FROM reactions WHERE user_id=%s AND card_id=%s",(current_user, card_id)
    )
    card_info = cursor.fetchone()
    user_id = card_info["user_id"] if card_info else None
    card_ID = card_info["card_id"] if card_info else None
    reaction = card_info["reaction"] if card_info else None
    
    if report:
        if user_id and card_ID:
            cursor.execute(
                "UPDATE reactions SET reported = %s WHERE user_id=%s AND card_id=%s",("TRUE", current_user, card_id)
            )
            mydb.commit()
        else:
            cursor.execute(
                "INSERT INTO reactions (user_id, card_id, reported) VALUES (%s, %s, %s)",(current_user, card_id, "TRUE")
            )
            mydb.commit()
            
        cursor.execute(
            "SELECT COUNT(*) as report_count FROM reactions WHERE card_id = %s AND reported = %s",
                (card_id, 'TRUE')
            )
        report_count = cursor.fetchone()["report_count"]
        if report_count == 1:
            cursor.execute(
                "DELETE FROM disaster_uploads WHERE image_id = %s",(card_id,)
            )
            cursor.execute(
                "DELETE FROM reactions WHERE card_id = %s",(card_id,)
            )
            mydb.commit()
            keys = await r.keys("feed:*")
            if keys:
                await r.delete(*keys)
            await card_del(card_id)
    else:
        if not reaction:
            cursor.execute(
                "DELETE FROM reactions WHERE user_id=%s AND card_id=%s",(current_user, card_id)
            )
            mydb.commit()
        else:
            cursor.execute(
                "UPDATE reactions SET reported = %s WHERE user_id=%s AND card_id=%s",(None, current_user, card_id)
            )
            mydb.commit()
            
@router.delete("/user/reports/delete")
async def del_reports(
    card_id : int,
    currentUserId : int
):
    cursor.execute(
        "DELETE FROM disaster_uploads WHERE image_id=%s",(card_id,)
    )
    cursor.execute(
        "DELETE FROM reactions WHERE card_id=%s",(card_id,)
    )
    mydb.commit()
    keys = await r.keys("feed:*")
    if keys:
        await r.delete(*keys)
    await card_del(card_id)
    return {"success" : True}