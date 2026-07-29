from main1 import app
from fastapi.testclient import TestClient
from database.database import cursor, mydb

client = TestClient(app)


def create_user(email):
    cursor.execute(
        """
        INSERT INTO users(email,name,google_id,profile_pic)
        VALUES(%s,%s,%s,%s)
        """,
        (
            email,
            "Test User",
            email,
            "test.jpg"
        )
    )

    mydb.commit()

    return cursor.lastrowid


def create_report(user_id):

    cursor.execute(
        """
        INSERT INTO disaster_uploads
        (user_id,image_path,disaster_type,latitude,longitude,description)
        VALUES(%s,%s,%s,%s,%s,%s)
        """,
        (
            user_id,
            "test.jpg",
            "Flood",
            10.1234,
            76.1234,
            "Test disaster report"
        )
    )

    mydb.commit()

    return cursor.lastrowid



def test_delete_own_report():

    user_id = create_user("owner@test.com")

    card_id = create_report(user_id)


    response = client.delete(
        f"/user/reports/delete?card_id={card_id}&currentUserId={user_id}"
    )


    assert response.status_code == 200



def test_delete_other_user_report():

    # Report owner
    owner_id = create_user("owner2@test.com")

    card_id = create_report(owner_id)


    # Another user
    other_user_id = create_user("other@test.com")


    response = client.delete(
        f"/user/reports/delete?card_id={card_id}&currentUserId={other_user_id}"
    )


    assert response.status_code == 403