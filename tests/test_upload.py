from fastapi.testclient import TestClient
from jwt.jwt_handler import create_access_token
from main1 import app
from database.database import cursor, mydb
import uuid

client = TestClient(app)


def create_test_user():

    unique = uuid.uuid4().hex

    cursor.execute(
        """
        INSERT INTO users
        (email, name, google_id, profile_pic)
        VALUES (%s,%s,%s,%s)
        """,
        (
            f"{unique}@test.com",
            "Upload Test User",
            f"google_{unique}",
            "test.jpg"
        )
    )

    mydb.commit()

    return cursor.lastrowid, f"{unique}@test.com"


def test_valid_image():

    user_id, email = create_test_user()

    token = create_access_token(
        data={
            "user_id": user_id,
            "sub": email
        }
    )

    with open("tests/test_image.jpeg", "rb") as image:

        files = {
            "File": (
                "test.jpg",
                image,
                "image/jpeg"
            )
        }

        data = {
            "latitude": "10.5276",
            "longitude": "76.2144"
        }

        response = client.post(
            "/demo",
            files=files,
            data=data,
            cookies={
                "access_token": token
            }
        )

    assert response.status_code == 200


def test_invalid_image():

    user_id, email = create_test_user()

    token = create_access_token(
        data={
            "user_id": user_id,
            "sub": email
        }
    )

    files = {
        "File": (
            "test.txt",
            b"fake_image",
            "image/jpeg"
        )
    }

    data = {
        "latitude": "10.5276",
        "longitude": "76.2144"
    }

    response = client.post(
        "/demo",
        files=files,
        data=data,
        cookies={
            "access_token": token
        }
    )

    assert response.status_code == 400