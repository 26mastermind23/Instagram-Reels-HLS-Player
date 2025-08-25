Instagram Reels HLS Player

This project allows you to play Instagram Reels directly on a custom website. It uses a React frontend and a Python FastAPI backend to download videos and serve them in HLS (.m3u8) format.

---

Features

- Input Instagram Reel URLs in a React frontend.
- Backend downloads video using yt-dlp.
- Converts video to HLS (.m3u8 + .ts chunks) using ffmpeg.
- Automatic cleanup of old videos (default: 30 minutes).
- Fully Dockerized — easy to run anywhere.
- Plays HLS streams in browser using hls.js.

---

Architecture

React Frontend
      |
      v
FastAPI Backend
      |
      v
yt-dlp + ffmpeg → HLS (.m3u8 + .ts)
      |
      v
Browser (hls.js)

Workflow:

1. User enters Instagram Reel URL in the React frontend.
2. Frontend sends POST request to /download API.
3. Backend downloads the video and converts it to HLS.
4. Backend returns .m3u8 playlist URL.
5. Frontend plays the HLS video using hls.js.
6. Old videos are automatically deleted after 30 minutes.

---

Technologies Used

- FastAPI – Backend API server.
- yt-dlp – Downloads Instagram Reels.
- ffmpeg – Converts video to HLS format.
- HLS.js – Plays HLS streams in the browser.
- React – Frontend UI.
- Docker + Docker Compose – Containerized environment.

---

Setup & Run

Requirements:

- Docker
- Docker Compose

Steps:

1. Clone the repository:

git clone https://github.com/26mastermind23/Instagram-Reels-HLS-Player

cd Instagram-Reels-HLS-Player

2. Build and start the containers:

docker-compose build
docker-compose up

3. Open the frontend:

http://localhost:3000

4. Paste a public Instagram Reel URL and click “Play”.

---

Stop the Project

docker-compose down

- Stops all containers.
- Add -v to remove volumes (including HLS video files):

docker-compose down -v

---

Notes on Private Reels

- This project only works with public Reels.
- Downloading private Reels requires authentication (cookies/session) and may violate Instagram’s Terms of Service.
- For private content, use your own account and session cookies with yt-dlp.

---
