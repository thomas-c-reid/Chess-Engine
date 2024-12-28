import React, { useState, useEffect } from "react";
import { FaLinkedin, FaInstagram, FaGithub } from 'react-icons/fa';
import './leftPanel.css';
import { postStartGame } from "../../services/apiHandler";

function LeftPanel({ playerOptions, gameOptions, gameStatus, connectToWebSocket, setGameStatus }) {
  const [selectedTime, setSelectedTime] = useState("5min");
  const [selectedStartOption, setSelectedStartOption] = useState("player_one_starts");
  const [selectedPlayerOne, setSelectedPlayerOne] = useState("");
  const [selectedPlayerTwo, setSelectedPlayerTwo] = useState("");

  const isStartDisabled = !selectedPlayerOne || !selectedPlayerTwo || !selectedTime || !selectedStartOption;

  const handleStartGame = async () => {
    const gameTime = selectedTime;
    const whoStarts = selectedStartOption;
    const playerOne = document.getElementById("playerOne").value;
    const playerTwo = document.getElementById("playerTwo").value;

    const payload = {
      selected_player_names: [playerOne, playerTwo],
      starts: whoStarts === "Random" ? "RAND" : whoStarts === "PlayerOne" ? "P1" : "P2",
      game_length: gameTime,
    };

    try {
      await postStartGame({ payload, connectToWebSocket, setGameStatus });
    } catch (err) {
      console.error("Error starting game:", err);
    }
  }

  return (
    <div className="left-panel">
      <h1 className="panel-header">Chess Arena</h1>

      {/* Dropdowns for player selection */}
      <div className="dropdown-group">
        <div className="dropdown-item">
          <label htmlFor="playerOne">Select Player 1:</label>
          <select
            id="playerOne"
            className="dropdown-menu"
            value={selectedPlayerOne}
            onChange={(e) => setSelectedPlayerOne(e.target.value)}
          >
            <option value="">-- Select Player 1 --</option>
            {playerOptions.length > 0 ? (
              playerOptions.map((agent, index) => (
                <option key={index} value={agent.name}>
                  {agent.name}
                </option>
              ))
            ) : (
              <option value="incorrectly loaded agent"></option>
            )}
          </select>
        </div>

        <div className="dropdown-item">
          <label htmlFor="playerTwo">Select Player 2:</label>
          <select
            id="playerTwo"
            className="dropdown-menu"
            value={selectedPlayerTwo}
            onChange={(e) => setSelectedPlayerTwo(e.target.value)}
          >
            <option value="">-- Select Player 2 --</option>
            {playerOptions.length > 0 ? (
              playerOptions.map((agent, index) => (
                <option key={index} value={agent.name}>
                  {agent.name}
                </option>
              ))
            ) : (
              <option value="incorrectly loaded agents"></option>
            )}
          </select>
        </div>
      </div>

      {/* Tabs for Game Time Options */}
        <div className="tab-group">
        <label htmlFor="timeOptions" className="tab-label">Select Game Time:</label>
        <div className="tabs-container">
            {gameOptions.time_options?.length > 0 ? (
            gameOptions.time_options.map((option, index) => (
                <div
                key={index}
                className={`tab-item ${selectedTime === option ? "active" : ""}`}
                onClick={() => setSelectedTime(option)}
                >
                {option}
                </div>
            ))
            ) : (
            <p>Loading...</p>
            )}
        </div>
        </div>

        {/* Tabs for starting options */}
        <div className="tab-group">
        <label htmlFor="whoStarts" className="tab-label">Who Starts:</label>
        <div className="tabs-container">
            {gameOptions.starting_options?.length > 0 ? (
            gameOptions.starting_options.map((option, index) => (
                <div
                key={index}
                className={`tab-item ${selectedStartOption === option ? "active" : ""}`}
                onClick={() => setSelectedStartOption(option)}
                >
                {option.replace(/_/g, " ")} {/* Replace underscores with spaces */}
                </div>
            ))
            ) : (
            <p>Loading...</p>
            )}
        </div>
        </div>

      {/* Start Match Button */}
      <div className="start-button">
        <button
          className={`start-match-btn ${isStartDisabled ? "disabled" : ""}`}
          disabled={isStartDisabled}
          onClick={() => handleStartGame()}
        >
          Start Match
        </button>
      </div>

      {/* Game Status Indicators */}
      <div className="game-status">
        <div className="status-item">
          <div className={`status-circle ${gameStatus.apiConnected ? "green" : "red"}`}></div>
          <span>Connected to API</span>
        </div>
        <div className="status-item">
          <div className={`status-circle ${gameStatus.websocketConnected ? "green" : "red"}`}></div>
          <span>Connected to WebSocket</span>
        </div>
        <div className="status-item">
          <div className={`status-circle ${gameStatus.gameInProgress ? "green" : "red"}`}></div>
          <span>Game in Progress</span>
        </div>
      </div>

      {/* Social Links */}
        <div className="bottom-links">
        <span>Thomas Reid 2025</span>
        <div className="social-icons">
            <a href="https://www.linkedin.com/in/thomas-reid-7298bb219/" target="_blank" rel="noopener noreferrer">
            <FaLinkedin size={20} />
            </a>
            <a href="https://www.instagram.com/thomas_reid10/" target="_blank" rel="noopener noreferrer">
            <FaInstagram size={20} />
            </a>
            <a href="https://github.com/thomas-c-reid" target="_blank" rel="noopener noreferrer">
            <FaGithub size={20} />
            </a>
        </div>
        </div>
    </div>
  );
}

export default LeftPanel;
