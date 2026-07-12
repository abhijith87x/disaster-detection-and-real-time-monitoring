from fastapi.testclient import TestClient
from main1 import socket_app

client = TestClient(socket_app)

def test_deletion():
    response = client.delete("/user/reports/delete?card_id=1&currentUserId=1")
    assert response.status_code == 200