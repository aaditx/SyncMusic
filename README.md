# SyncSound

A collaborative music-sharing app built with Python (FastAPI). Users can join rooms, chat, and listen to synchronized music.

## Features

- **Real-time Sync**: Playback is synchronized across all clients using WebSockets.
- **Chat**: Simple text chat in rooms.
- **Playlist**: Add tracks via URL (Direct MP3/MP4 or YouTube).
- **Python Only**: Backend serves a static HTML/JS client.

## Tech Stack

- **Backend**: Python 3.11+, FastAPI, Uvicorn
- **Real-time**: WebSockets
- **Frontend**: Vanilla HTML/JS (served by FastAPI)
- **Infrastructure**: Docker Compose

## Setup & Running

### Prerequisites

- Python 3.11+
- Docker (optional)

### Local Development

1.  **Install Dependencies**:
    ```bash
    cd backend
    pip install -r requirements.txt
    ```

2.  **Run Server**:
    ```bash
    uvicorn app.main:app --reload
    ```

3.  **Access App**:
    Open `http://localhost:8000` in your browser.

### Docker

1.  **Run with Docker Compose**:
    ```bash
    docker-compose up --build
    ```

2.  **Access App**:
    Open `http://localhost:8000` in your browser.

## Usage

1.  **Create a Room**: Enter a name and click "Create Room".
2.  **Share URL**: Copy the URL (or Room ID) and send it to a friend.
3.  **Add Tracks**: Paste a direct URL to an audio/video file (e.g., `https://example.com/song.mp3`) or a YouTube link.
4.  **Play/Pause/Seek**: Controls are synchronized.

## Testing

Run the backend tests:

```bash
cd backend
pytest
```

## Legal Note

This project is for educational purposes.
- Respect platform Terms of Service.
- Do not use for copyright infringement.
- Only stream content you have rights to.

## License

MIT
