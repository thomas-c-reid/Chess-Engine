import React, { useState, useEffect } from "react";
import "./playerinfo.css";

function PlayerInfo({ playerData, name }) {
  const [playerName, setPlayerName] = useState('');
  const [playerBio, setPlayerBio] = useState('');
  const [playerPhoto, setPlayerPhoto] = useState(null); // Store the photo URL

  useEffect(() => {
    const player = playerData.find((p) => p.colour === name);
    if (player) {
      setPlayerName(player.name || '');
      setPlayerBio(player.bio || '');
      setPlayerPhoto(player.photo || null); // Set the photo URL if available
    }
  }, [playerData, name]);

  return (
    <div className="player-info">
      <div
        className="player-icon"
        style={{
          backgroundImage: playerPhoto ? `url(${playerPhoto})` : null,
        }}
      ></div>
      <div className="player-details">
        <p className="player-name">{playerName}</p>
        <p className="player-bio">{playerBio}</p>
      </div>
    </div>
  );
}

export default PlayerInfo;
