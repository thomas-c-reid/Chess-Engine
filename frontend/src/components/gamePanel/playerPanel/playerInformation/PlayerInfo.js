import React from "react";
import "./playerinfo.css";

function PlayerInfo({ playerName }) {
  return (
    <div className="player-info">
      <div className="player-icon"></div>
      <div className="player-details">
        <p className="player-name">{playerName}</p>
        <p className="player-bio">Player bio goes here</p>
      </div>
    </div>
  );
}

export default PlayerInfo;
