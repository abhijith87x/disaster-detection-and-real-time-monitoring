from fastapi.testclient import TestClient
from main1 import app
from jwt.jwt_handler import create_access_token

client = TestClient(app)

def test_no_token():
    response = client.get("/profile")
    assert response.status_code == 401
    
def test_valid_token():
    token = create_access_token(
         data={
            "sub": "abhijith87b@gmail.com",
            "user_id" : 1
         }
    )
    
    response = client.get(
        '/profile',
        cookies={
            "access_token" : token
        }
    )
    assert response.status_code == 200