import React, { useState } from "react";
import Hls from "hls.js";

function App() {
  const [url, setUrl] = useState("");
  const [videoSrc, setVideoSrc] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await fetch("http://localhost:8000/download", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });
    const data = await res.json();
    if (data.playlist) {
      setVideoSrc("http://localhost:8000" + data.playlist);
    }
  };

  React.useEffect(() => {
    if (videoSrc && Hls.isSupported()) {
      const video = document.getElementById("video");
      const hls = new Hls();
      hls.loadSource(videoSrc);
      hls.attachMedia(video);
    }
  }, [videoSrc]);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Instagram Reel Player</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter Instagram Reel URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          style={{ width: "400px", marginRight: "1rem" }}
        />
        <button type="submit">Play</button>
      </form>
      <div style={{ marginTop: "2rem" }}>
        {videoSrc && (
          <video
            id="video"
            controls
            autoPlay
            style={{ width: "100%", maxWidth: "600px" }}
          />
        )}
      </div>
    </div>
  );
}

export default App;
