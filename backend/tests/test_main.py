from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    # Should return index.html content
    assert "<!DOCTYPE html>" in response.text

def test_create_room():
    response = client.post("/api/rooms?name=TestRoom")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "TestRoom"
    assert "id" in data

def test_list_rooms():
    # Ensure at least one room exists from previous test
    client.post("/api/rooms?name=Room1")
    response = client.get("/api/rooms")
    assert response.status_code == 200
    assert len(response.json()) > 0
