import React, { useState } from "react";
import "./App.css";

function App() {
  const [movie, setMovie] = useState("");
  const [recommendations, setRecommendations] = useState([]);

  const getRecommendations = async () => {
    const res = await fetch("http://127.0.0.1:5000/recommend", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ movie }),
    });

    const data = await res.json();
    setRecommendations(data);
  };

  return (
    <div className="App">
      <h1>🎬 Movie Recommender</h1>

      <input
        type="text"
        placeholder="Enter movie name..."
        value={movie}
        onChange={(e) => setMovie(e.target.value)}
      />

      <button onClick={getRecommendations}>Recommend</button>

      <div className="movie-list">
        {recommendations.map((item, index) => (
          <div className="movie-card" key={index}>
            <div className="movie-title">{item.title}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;