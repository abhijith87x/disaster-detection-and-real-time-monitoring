from main1 import app
from fastapi.testclient import TestClient
from database.database import cursor, mydb
import uuid

client = TestClient(app)


def create_test_data():

    # Create unique user
    email = f"{uuid.uuid4()}@test.com"
    google_id = str(uuid.uuid4())

    cursor.execute(
        """
        INSERT INTO users
        (email, name, google_id, profile_pic)
        VALUES (%s,%s,%s,%s)
        """,
        (
            email,
            "Reaction User",
            google_id,
            "test.jpg"
        )
    )

    mydb.commit()

    user_id = cursor.lastrowid

    # Create report
    cursor.execute(
        """
        INSERT INTO disaster_uploads
        (user_id, image_path, disaster_type, latitude, longitude, description)
        VALUES (%s,%s,%s,%s,%s,%s)
        """,
        (
            user_id,
            "test.jpg",
            "Flood",
            10.1234,
            76.1234,
            "test_description"
        )
    )

    mydb.commit()

    card_id = cursor.lastrowid

    return user_id, card_id


def test_like_report():

    user_id, card_id = create_test_data()

    response = client.post(
        f"/user/like/update?current_user={user_id}&card_id={card_id}&like=True"
    )

    assert response.status_code == 200


def test_dislike_report():

    user_id, card_id = create_test_data()

    response = client.post(
        f"/user/dislike/update?current_user={user_id}&card_id={card_id}&dislike=True&type=tsunami"
    )

    assert response.status_code == 200


def test_report():

    user_id, card_id = create_test_data()

    response = client.post(
        f"/user/report/update?current_user={user_id}&card_id={card_id}&report=True"
    )

    assert response.status_code == 200