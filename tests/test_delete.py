from fastapi.testclient import TestClient
from main1 import app
from database.database import cursor, mydb
import uuid

client = TestClient(app)


def create_user(email):
    google_id = str(uuid.uuid4())

    cursor.execute(
        """
        INSERT INTO users
        (email, name, google_id, profile_pic)
        VALUES (%s, %s, %s, %s)
        """,
        (
            email,
            "Test User",
            google_id,
            "test.jpg"
        )
    )

    mydb.commit()

    return cursor.lastrowid


def create_report(user_id):

    file_path = "https://test-bucket/test_image.jpeg"

    cursor.execute(
        """
        INSERT INTO disaster_uploads
        (user_id, image_path, disaster_type, latitude, longitude, description)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            user_id,
            file_path,
            "Flood",
            10.1234,
            76.1234,
            "Test disaster report"
        )
    )

    mydb.commit()

    return cursor.lastrowid


def test_delete_own_report():

    owner_email = f"{uuid.uuid4()}@test.com"
    user_id = create_user(owner_email)

    card_id = create_report(user_id)

    response = client.delete(
        f"/user/reports/delete?card_id={card_id}&currentUserId={user_id}"
    )

    assert response.status_code == 200


def test_delete_other_user_report():

    owner_email = f"{uuid.uuid4()}@test.com"
    owner_id = create_user(owner_email)

    card_id = create_report(owner_id)

    other_email = f"{uuid.uuid4()}@test.com"
    other_user_id = create_user(other_email)

    response = client.delete(
        f"/user/reports/delete?card_id={card_id}&currentUserId={other_user_id}"
    )

    assert response.status_code == 403