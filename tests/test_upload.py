from auth_jwt_helper.jwt_handler import create_access_token
from database import get_oauth_db
import uuid, requests

def create_test_user():
    
    email = f"{uuid.uuid4()}@test.com"
    google_id = str(uuid.uuid4())

    db = get_oauth_db()
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

    response = requests.post(
        "http://localhost:8002/demo",
        files=files,
        data=data,
        cookies={
            "access_token": token
        }
    )

    assert response.status_code == 400