from fastapi.testclient import TestClient
from jwt.jwt_handler import create_access_token
from main1 import app

client = TestClient(app)

def test_valid_image():
    with open("tests/test_image.jpeg", "rb") as image:
        files = {
            "File": (
                "test.jpg",
                image,
                "image/jpeg"
            )
        }
        data = {
            "latitude": "10.5276",
            "longitude": "76.2144"
        }
    
        token =  create_access_token(
            data={
                "user_id" : "1",
                "sub":"abhijith87b@gmail.com"
            }
        )
        
        response = client.post(
            "/demo",
            files=files,
            data=data,
            cookies={
                "access_token":token
            }
        )
        
        assert response.status_code == 200
        
def test_invalid_image():

    files = {
        "File": (
            "test.txt",
            b"fake_image",
            "image/jpeg"
        )
    }
    data = {
        "latitude": "10.5276",
        "longitude": "76.2144"
    }
        
    token = create_access_token(
        data={
            "user_id" : "1",
            "sub" : "abhijith87b@gamil.com"
            }
        )
        
    response = client.post(
        "/demo",
        files=files,
        data=data,
        cookies={
                "access_token":token
            }
        )
        
    assert response.status_code == 400
        