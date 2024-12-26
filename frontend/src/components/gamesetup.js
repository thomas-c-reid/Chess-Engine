import '../css/gameSetup.css';
import React, { useState, useEffect } from "react";
const { io } = require("socket.io-client")


function GameSetup({playerOptions, connectToWebSocket}) {
    const [gameStatus, setGameStatus] = useState(""); // For API feedback
    const [moves, setMoves] = useState([]); // List of moves received
    const [socket, setSocket] = useState(null); // WebSocket connection

    const handleStartGame = async () => {

        const playerOne = document.getElementById("playerOne").value;
        const playerTwo = document.getElementById("playerTwo").value;
        const gameTime = document.getElementById("gameTime").value;
        const whoStarts = document.getElementById("whoStarts").value;

        const payload = {
            selected_player_names: [playerOne, playerTwo],
            starts: whoStarts === "Random" ? "RAND" : whoStarts === "PlayerOne" ? "P1" : "P2",
            game_length: gameTime,
        };

        try {
            // POST to Flask API to start the game
            const response = await fetch("http://localhost:5000/api/start-match", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(payload),
            });

            if (response['status'] == 200) {
                setGameStatus('Connection established')
            } else {
                setGameStatus('Connection failed', response['status'])
            }

            if (connectToWebSocket) {
                connectToWebSocket();
                console.log(connectToWebSocket)
            } else {
                console.error('FAILED TO ESTABLISH WEBSOCKET CONNECTION');
            }

        } catch (err) {
            console.error("Error starting game:", err);
            setGameStatus("Failed to start game.");
        }
    }

    return (
      <div className="game-setup-panel">
        <h1 className="header-title">Chess Engine</h1>

        {/* player selection */}

        <div className="dropdown-group">
            <div className="dropdown-item">
                <label htmlFor='playerOne'>Select Player One:</label>
                <select id="playerOne" className="dropdown-menu">
                    {playerOptions.length > 0 ? (
                        playerOptions.map((agent, index) => (
                            <option key={index} value={agent.name}>
                                {agent.name}
                            </option>
                        ))
                    ) : (
                        <option value="incorectly loaded agent"></option>
                    )}
                </select>
            </div>

            <div className="dropdown-item">
                <label htmlFor='playerTwo'>Select Player Two:</label>
                <select id="playerTwo" className='dropdown-menu'>
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
        </div>

        {/* Game Config Section */}

        <div className="game-config">
            <h2>Game Config</h2>

            <div className="dropdown-item">
                <label htmlFor="gameTime">Select Time:</label>
                <select id="gameTime" className="dropdown-menu">
                    <option value="5min">5 Minutes</option>
                    <option value="10min">10 Minutes</option>
                    <option value="15min">15 Minutes</option>
                </select>
            </div>

            <div className="dropdown-item">
                <label htmlFor="whoStarts">Who Starts as White:</label>
                <select id="whoStarts" className="dropdown-menu">
                    <option value="PlayerOne">Player One</option>
                    <option value="PlayerTwo">Player Two</option>
                    <option value="Random">Random</option>
                </select>
            </div>
        </div>

        <div className='button-container'>
            <button className="start-game-button" onClick={handleStartGame}>Start Game</button>
        </div>

        {/* Game Status and Moves */}
        <div className="game-status">
                <h3>Status: {gameStatus}</h3>
                <h4>Moves:</h4>
                <ul>
                    {moves.map((move, index) => (
                        <li key={index}>{move}</li>
                    ))}
                </ul>
            </div>

      </div>
  
      
    );
  }
  
  export default GameSetup;