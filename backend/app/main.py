from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List
import uuid
import os

from .ws import manager
from .models import Room, Track

app = FastAPI(title="SyncSound API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Endpoints
@app.get("/api/rooms", response_model=List[Room])
async def list_rooms():
    return list(manager.rooms.values())

@app.post("/api/rooms")
async def create_room(name: str):
    room_id = str(uuid.uuid4())[:8]
    room = Room(id=room_id, name=name)
    manager.rooms[room_id] = room
    return room

@app.get("/api/rooms/{room_id}", response_model=Room)
async def get_room(room_id: str):
    if room_id not in manager.rooms:
        raise HTTPException(status_code=404, detail="Room not found")
    return manager.rooms[room_id]

@app.websocket("/ws/{room_id}/{client_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, client_id: str):
    await manager.connect(websocket, room_id, client_id)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.handle_command(room_id, client_id, data)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)

# Serve Static Files
# Ensure the static directory exists
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/{full_path:path}")
async def serve_app(full_path: str):
    # Serve index.html for any path not matched by API (SPA-like behavior for static client)
    # But since we are doing simple static, we can just serve index.html at root
    # and let the client handle "routing" via query params or hash if needed.
    # For simplicity, we'll just serve index.html at root.
    return FileResponse(os.path.join(static_dir, "index.html"))
