from main1 import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_like_report():
    response = client.post(
        '/user/like/update?current_user=5&card_id=23&like=True'
    )
    assert response.status_code == 200
    
def test_dislike_report():
    response = client.post(
        '/user/dislike/update?current_user=5&card_id=23&dislike=True&type=tsunami'
    )
    assert response.status_code == 200
    
def test_report():
    response = client.post(
        '/user/report/update?current_user=5&card_id=23&report=True'
    )
    assert response.status_code == 200