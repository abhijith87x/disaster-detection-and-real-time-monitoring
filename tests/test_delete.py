from main1 import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_delete_own_report():
    response = client.delete(
        '/user/reports/delete?card_id=22&currentUserId=1'
    )
    assert response.status_code == 200
    
def test_delete_other_user_report():
    response = client.delete(
        '/user/reports/delete?card_id=22&currentUserId=44'
    )
    assert response.status_code == 200