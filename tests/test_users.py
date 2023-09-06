from .database import client, session
from app import schemas

def test_root(client):
    resp = client.get("/")
    # print(resp.json().get("message"))
    
    assert resp.json().get("message") == "Hello World"
    assert resp.status_code == 200

def test_create_user(client):
    resp = client.post("/users", json={"email":"test@gmail.com", "password":"123"})
    # print("RESPONSE: ",resp.json())
    new_user = schemas.UserOut(**resp.json())

    assert new_user.email == "test@gmail.com"
    assert resp.status_code == 201

def test_login_user(client):

    resp = client.post("/login", data={"username": "test@gmail.com", "password": "123"})

    assert resp.status_code == 200
    

