from fastapi.testclient import TestClient
from auth_jwt.jwt_handler import create_access_token
from main1 import app
from database.database import get_db
import uuid

client = TestClient(app)


# def create_test_user():

#     email = f"{uuid.uuid4()}@test.com"
#     google_id = str(uuid.uuid4())

#     cursor.execute(
#         """
#         INSERT INTO users
#         (email, name, google_id, profile_pic)
#         VALUES (%s,%s,%s,%s)
#         """,
#         (
#             email,
#             "Upload Test User",
#             google_id,
#             "test.jpg"
#         )
#     )

#     mydb.commit()

#     return cursor.lastrowid, email


def create_test_user():
    email = f"{uuid.uuid4()}@test.com"
    google_id = str(uuid.uuid4())

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO users
        (email, name, google_id, profile_pic)
        VALUES (%s,%s,%s,%s)
        """,
        (
            email,
            "Upload Test User",
            google_id,
            "test.jpg"
        )
    )

    db.commit()

    user_id = cursor.lastrowid

    cursor.close()
    db.close()

    return user_id, email

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
            "text/plain"
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