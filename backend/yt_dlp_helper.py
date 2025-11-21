import sys
import json
import subprocess
from typing import Optional

"""
LEGAL DISCLAIMER AND USAGE WARNING
==================================

This script uses yt-dlp to extract media URLs. 
By using this software, you agree to the following:

1. You will NOT use this tool to download, reproduce, or redistribute copyrighted material 
   without the explicit permission of the rights holder.
2. You will respect the Terms of Service of any platform you interact with (e.g., YouTube).
3. This tool is intended for:
   - Personal consumption where allowed by law.
   - Streaming content for which you hold the rights.
   - Testing with public domain or Creative Commons content.
4. The developers of SyncSound assume no liability for misuse of this tool.

If you do not agree to these terms, do not use this script.
"""

def get_stream_url(url: str) -> Optional[dict]:
    """
    Get the direct stream URL for a given video URL using yt-dlp.
    This does NOT download the file, it only extracts the playback URL.
    """
    try:
        cmd = [
            "yt-dlp",
            "--dump-json",
            "--no-playlist",
            "--format", "bestaudio[ext=m4a]/bestaudio/best",  # Prefer audio
            url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        
        return {
            "title": data.get("title"),
            "url": data.get("url"),
            "duration": data.get("duration"),
            "thumbnail": data.get("thumbnail"),
            "webpage_url": data.get("webpage_url")
        }
        
    except subprocess.CalledProcessError as e:
        print(f"Error extracting URL: {e.stderr}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python yt_dlp_helper.py <video_url>")
        sys.exit(1)
        
    video_url = sys.argv[1]
    print("Fetching stream info... Please ensure you have rights to access this content.")
    info = get_stream_url(video_url)
    
    if info:
        print(json.dumps(info, indent=2))
    else:
        sys.exit(1)
