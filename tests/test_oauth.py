from auth_jwt_helper.jwt_handler import create_access_token
from database import get_oauth_db
from utils.aws_s3 import upload_file_to_s3
import requests
def create_test_user():
    
    db = get_oauth_db()
    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO users
        (email, name, google_id, profile_pic)
        VALUES (%s,%s,%s,%s)
        """,
        (
            "oauth11test@gmail.com",
            "OAuth Test User",
            "google_oauth_test",
            "test.jpg"
        )
    )

    db.commit()
    user_id = cursor.lastrowid

    cursor.close()
    db.close()

    return user_id


def test_no_token():

    response = requests.get("/profile")

    assert response.status_code == 401



def test_valid_token():

    # Create user
    user_id = create_test_user()


    token = create_access_token(
        data={
            "sub": "oauth_test@gmail.com",
            "user_id": user_id
        }
    )


    response = requests.get(
        "/profile",
        cookies={
            "access_token": token
        }
    )


    assert response.status_code == 200