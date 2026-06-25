from fastapi import APIRouter
from database.database import cursor,mydb
from socket_app.feed_updates import card_del
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
        print("reported",reported)
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
@router.post("/user/dislike/update") 
async def dislike_update(
    current_user : int,
    card_id : int,
    dislike : bool,
    type : str
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
    else:
        if not reported:
            cursor.execute(
                "DELETE FROM reactions WHERE user_id=%s AND card_id=%s",(current_user, card_id)
            )
            mydb.commit()
        else:
            cursor.execute(
                "UPDATE reactions SET reaction = %s , suggested_type=%s WHERE user_id=%s AND card_id=%s",(None, None, current_user, card_id)
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
        "DELETE FROM disaster_uploads WHERE image_id=%s AND user_id=%s",(card_id,currentUserId)
    )
    cursor.execute(
        "DELETE FROM reactions WHERE card_id=%s",(card_id,)
    )
    mydb.commit()
    await card_del(card_id)
    return {"success" : True}