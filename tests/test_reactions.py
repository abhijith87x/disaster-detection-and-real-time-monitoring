from database import get_oauth_db, get_disaster_db
import uuid, requests

def create_test_data():
    db = get_oauth_db()
    cursor = db.cursor()

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

    db.commit()

    user_id = cursor.lastrowid
    
    disaster_db = get_disaster_db()
    d_cursor = disaster_db.cursor()
    
    d_cursor.execute(
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

    disaster_db.commit()

    card_id = d_cursor.lastrowid
    
    cursor.close()
    db.close()
    
    d_cursor.close()
    disaster_db.close()

    return user_id, card_id

def test_like_report():

    user_id, card_id = create_test_data()

    response = requests.post(
        f"http://localhost:8002/user/like/update?current_user={user_id}&card_id={card_id}&like=True"
    )

    assert response.status_code == 200


def test_dislike_report():

    user_id, card_id = create_test_data()

    response = requests.post(
        f"http://localhost:8002/user/dislike/update?current_user={user_id}&card_id={card_id}&dislike=True&type=tsunami"
    )

    assert response.status_code == 200


def test_report():

    user_id, card_id = create_test_data()

    response = requests.post(
        f"http://localhost:8002/user/report/update?current_user={user_id}&card_id={card_id}&report=True"
    )

    assert response.status_code == 200