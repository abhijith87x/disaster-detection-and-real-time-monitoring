from database import get_disaster_db, get_oauth_db
import uuid
import requests

def create_user(email):
    google_id = str(uuid.uuid4())

    mydb = get_oauth_db()
    cursor = mydb.cursor()

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

    user_id = cursor.lastrowid

    cursor.close()
    mydb.close()

    return user_id



def create_report(user_id):
    file_path = "https://test-bucket.s3.amazonaws.com/test_image.jpeg"

    mydb = get_disaster_db()
    cursor = mydb.cursor()

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

    card_id = cursor.lastrowid

    cursor.close()
    mydb.close()

    return card_id

def test_delete_own_report():
    BASE_URL = "http://localhost:8002"
    owner_email = f"{uuid.uuid4()}@test.com"
    print("1")
    user_id = create_user(owner_email)
    print("2")
    card_id = create_report(user_id)

    response = requests.delete(
        f"{BASE_URL}/user/reports/delete?card_id={card_id}&currentUserId={user_id}"
    )

    assert response.status_code == 200


def test_delete_other_user_report():

    BASE_URL = "http://localhost:8002"
    owner_email = f"{uuid.uuid4()}@test.com"
    owner_id = create_user(owner_email)

    card_id = create_report(owner_id)

    other_email = f"{uuid.uuid4()}@test.com"
    other_user_id = create_user(other_email)

    response = requests.delete(
        f"{BASE_URL}/user/reports/delete?card_id={card_id}&currentUserId={other_user_id}"
    )

    assert response.status_code == 403