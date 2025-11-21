import os
from pydantic import BaseModel

class Settings(BaseModel):
    APP_NAME: str = "SyncSound"
    VERSION: str = "0.1.0"
    DEBUG: bool = True
    CORS_ORIGINS: list[str] = ["*"]
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Sync settings
    SYNC_INTERVAL_MS: int = 1000  # How often to broadcast state
    MAX_DRIFT_MS: int = 500       # Max allowed drift before hard correction

settings = Settings()
