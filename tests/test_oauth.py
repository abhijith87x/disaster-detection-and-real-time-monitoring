from fastapi.testclient import TestClient
from main1 import app
from jwt.jwt_handler import create_access_token
from database.database import cursor, mydb
from utils.aws_s3 import upload_file_to_s3


client = TestClient(app)


def create_test_user():
    
    
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

    mydb.commit()

    return cursor.lastrowid



def test_no_token():

    response = client.get("/profile")

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


    response = client.get(
        "/profile",
        cookies={
            "access_token": token
        }
    )


    assert response.status_code == 200