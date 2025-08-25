from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import subprocess, uuid, shutil, os, time
from pathlib import Path
import threading

app = FastAPI()

# Allow CORS for React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).parent
STREAMS_DIR = BASE_DIR / "streams"
STREAMS_DIR.mkdir(exist_ok=True)

EXPIRATION_SECONDS = 1800  # 30 minutes


def cleanup_old_streams():
    """Background thread to clean old streams"""
    while True:
        now = time.time()
        for folder in STREAMS_DIR.iterdir():
            if folder.is_dir():
                age = now - folder.stat().st_mtime
                if age > EXPIRATION_SECONDS:
                    shutil.rmtree(folder, ignore_errors=True)
                    print(f"[CLEANUP] Removed old stream folder: {folder}")
        time.sleep(300)  # run every 5 minutes


@app.on_event("startup")
def start_cleanup_thread():
    thread = threading.Thread(target=cleanup_old_streams, daemon=True)
    thread.start()


@app.post("/download")
async def download_reel(request: Request):
    data = await request.json()
    url = data.get("url")
    if not url:
        return JSONResponse({"error": "Missing URL"}, status_code=400)

    stream_id = str(uuid.uuid4())
    out_dir = STREAMS_DIR / stream_id
    out_dir.mkdir(exist_ok=True)

    mp4_file = out_dir / "video.mp4"
    m3u8_path = out_dir / "index.m3u8"

    # 1. Download best mp4
    subprocess.run([
        "yt-dlp", "-f", "best[ext=mp4]",
        "-o", str(mp4_file), url
    ], check=True)

    # 2. Convert to HLS (m3u8)
    subprocess.run([
        "ffmpeg", "-i", str(mp4_file),
        "-codec", "copy", "-start_number", "0",
        "-hls_time", "4", "-hls_list_size", "0",
        "-f", "hls", str(m3u8_path)
    ], check=True)

    return {"playlist": f"/streams/{stream_id}/index.m3u8"}


@app.get("/streams/{stream_id}/{filename}")
async def serve_stream(stream_id: str, filename: str):
    file_path = STREAMS_DIR / stream_id / filename
    if file_path.exists():
        return FileResponse(file_path)
    return JSONResponse({"error": "File not found"}, status_code=404)
