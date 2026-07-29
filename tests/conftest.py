from database.database import cursor,mydb
import pytest

cursor.execute(
    """
    INSERT INTO users (email, name, google_id, profile_pic)
    VALUES (%s, %s, %s, %s)
    """,
    (
        "test@test.com",
        "Test User",
        "google_test_123",
        "test.jpg"
    )
)

cursor.execute(
    """
    INSERT INTO disaster_uploads
    (user_id, image_path, disaster_type, latitude, longitude, description)
    VALUES (%s, %s, %s, %s, %s, %s)
    """,
    (
        1,
        "test.jpg",
        "Flood",
        10.1234,
        76.1234,
        "Test disaster report"
    )
)

mydb.commit()

card_id = cursor.lastrowid

cursor.execute(
    """
    INSERT INTO reactions (user_id, card_id, reaction)
    VALUES (%s, %s, %s)
    """,
    (
        1,
        card_id,
        "LIKE"
    )
)
mydb.commit()

cursor.execute(
    """
    INSERT INTO reactions
    (user_id, card_id, reaction, suggested_type)
    VALUES (%s, %s, %s, %s)
    """,
    (
        1,
        card_id,
        "DISLIKE",
        "Wildfire"
    )
)

mydb.commit()