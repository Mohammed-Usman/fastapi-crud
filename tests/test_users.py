from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    resp = client.get("/")
    # print(resp.json().get("message"))
    assert resp.json().get("message") == "Hello World"
    assert resp.status_code == 200