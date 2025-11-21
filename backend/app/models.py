from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Track(BaseModel):
    url: str
    title: str = "Unknown Track"
    duration: float = 0.0
    added_by: str
    thumbnail: Optional[str] = None

class Message(BaseModel):
    sender: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class RoomState(BaseModel):
    is_playing: bool = False
    current_track_index: int = -1
    position: float = 0.0
    last_updated: float = 0.0  # Server timestamp

class Room(BaseModel):
    id: str
    name: str
    playlist: List[Track] = []
    state: RoomState = Field(default_factory=RoomState)
    # In-memory only, not serialized usually, but good for debug
    connected_clients: int = 0

class SyncEvent(BaseModel):
    type: str  # 'chat', 'state_update', 'playlist_update', 'error'
    payload: dict
    timestamp: float = Field(default_factory=lambda: datetime.utcnow().timestamp())
