from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def test_websocket_connection():
    # Create a room first
    response = client.post("/api/rooms?name=WSRoom")
    room_id = response.json()["id"]
    
    with client.websocket_connect(f"/ws/{room_id}/user1") as websocket:
        # Should receive initial state
        data = websocket.receive_json()
        assert data["type"] == "state_update"
        
        data = websocket.receive_json()
        assert data["type"] == "playlist_update"
        
        # Send chat
        websocket.send_json({"type": "chat", "payload": {"content": "Hello"}})
        
        # Receive chat back
        data = websocket.receive_json()
        assert data["type"] == "chat"
        assert data["payload"]["content"] == "Hello"
