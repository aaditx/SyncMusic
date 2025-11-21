import time
from .models import RoomState

class SyncLogic:
    @staticmethod
    def get_current_server_time() -> float:
        return time.time()

    @staticmethod
    def calculate_current_position(state: RoomState) -> float:
        if not state.is_playing:
            return state.position
        
        elapsed = SyncLogic.get_current_server_time() - state.last_updated
        return state.position + elapsed

    @staticmethod
    def update_room_state(current_state: RoomState, new_state_dict: dict) -> RoomState:
        """
        Updates the room state based on a command.
        This is the authoritative state transition.
        """
        now = SyncLogic.get_current_server_time()
        
        # If we were playing, update the position up to 'now' before changing state
        if current_state.is_playing:
            current_state.position += (now - current_state.last_updated)
        
        # Apply changes
        if 'is_playing' in new_state_dict:
            current_state.is_playing = new_state_dict['is_playing']
        
        if 'position' in new_state_dict:
            current_state.position = new_state_dict['position']
            
        if 'current_track_index' in new_state_dict:
            current_state.current_track_index = new_state_dict['current_track_index']
            # Reset position on track change if not specified
            if 'position' not in new_state_dict:
                current_state.position = 0.0

        current_state.last_updated = now
        return current_state
