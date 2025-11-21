from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List
import json
import time
from .models import Room, Message, SyncEvent, RoomState, Track
from .sync import SyncLogic

class ConnectionManager:
    def __init__(self):
        # room_id -> List[WebSocket]
        self.active_connections: Dict[str, List[WebSocket]] = {}
        # room_id -> Room
        self.rooms: Dict[str, Room] = {}

    async def connect(self, websocket: WebSocket, room_id: str, client_id: str):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
            # Initialize room if not exists (in-memory for now)
            if room_id not in self.rooms:
                self.rooms[room_id] = Room(id=room_id, name=f"Room {room_id}")
        
        self.active_connections[room_id].append(websocket)
        self.rooms[room_id].connected_clients += 1
        
        # Send initial state
        await self.send_personal_message(
            websocket,
            SyncEvent(type="state_update", payload=self.rooms[room_id].state.model_dump()).model_dump()
        )
        await self.send_personal_message(
            websocket,
            SyncEvent(type="playlist_update", payload={"playlist": [t.model_dump() for t in self.rooms[room_id].playlist]}).model_dump()
        )

    def disconnect(self, websocket: WebSocket, room_id: str):
        if room_id in self.active_connections:
            if websocket in self.active_connections[room_id]:
                self.active_connections[room_id].remove(websocket)
                if room_id in self.rooms:
                    self.rooms[room_id].connected_clients -= 1
                    if self.rooms[room_id].connected_clients <= 0:
                        # Optional: Clean up empty rooms after delay? 
                        # For now, keep them.
                        pass

    async def send_personal_message(self, websocket: WebSocket, message: dict):
        await websocket.send_json(message)

    async def broadcast(self, room_id: str, message: dict):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                try:
                    await connection.send_json(message)
                except RuntimeError:
                    # Connection might be closed
                    pass

    async def handle_command(self, room_id: str, client_id: str, data: dict):
        if room_id not in self.rooms:
            return

        room = self.rooms[room_id]
        command_type = data.get("type")
        payload = data.get("payload", {})

        if command_type == "chat":
            msg = Message(sender=client_id, content=payload.get("content", ""))
            event = SyncEvent(type="chat", payload=msg.model_dump())
            await self.broadcast(room_id, event.model_dump())

        elif command_type == "play":
            new_state = {"is_playing": True}
            # If starting from specific position
            if "position" in payload:
                new_state["position"] = payload["position"]
            
            room.state = SyncLogic.update_room_state(room.state, new_state)
            await self.broadcast_state(room_id)

        elif command_type == "pause":
            new_state = {"is_playing": False}
            room.state = SyncLogic.update_room_state(room.state, new_state)
            await self.broadcast_state(room_id)

        elif command_type == "seek":
            new_state = {"position": payload.get("position", 0.0)}
            room.state = SyncLogic.update_room_state(room.state, new_state)
            await self.broadcast_state(room_id)
            
        elif command_type == "add_track":
            track = Track(**payload)
            room.playlist.append(track)
            await self.broadcast(room_id, SyncEvent(type="playlist_update", payload={"playlist": [t.model_dump() for t in room.playlist]}).model_dump())

        elif command_type == "change_track":
            index = payload.get("index", 0)
            if 0 <= index < len(room.playlist):
                new_state = {"current_track_index": index, "position": 0.0, "is_playing": True}
                room.state = SyncLogic.update_room_state(room.state, new_state)
                await self.broadcast_state(room_id)

    async def broadcast_state(self, room_id: str):
        if room_id in self.rooms:
            state = self.rooms[room_id].state
            event = SyncEvent(type="state_update", payload=state.model_dump())
            await self.broadcast(room_id, event.model_dump())

manager = ConnectionManager()
