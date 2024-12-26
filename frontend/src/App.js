// App.js

import './App.css';
import GameSetup from './components/gamesetup.js';
import Board from './components/board.js';
import WebSocketHandler from './components/websocketHandler.js';
import React, { useState, useEffect } from "react";
import { Chess } from 'chess.js';
import yaml from 'js-yaml';
import LeftPanel from './components/leftPanel.js'
import MainSection from './components/mainSection.js';

function App() {
  const [moves, setMoves] = useState([]);
  const [game, setGame] = useState(new Chess());
  const [playerOptions, setPlayerOptions] = useState([]);
  const [gameOptions, setGameOptions] = useState([]);
  const [connectWebSocketFunc, setConnectWebSocketFunc] = useState(null);
  const [fenstring, setFenstring] = useState("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1");
  const [gameStatus, setGameStatus] = useState({
    apiConnected: false,
    websocketConnected: false,
    gameInProgress: false,
  });

  const loadPlayerOptions = async () => {
    const url = '/agent_info.yaml';
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Failed to fetch YAML file: ${response.statusText}`);
    }
    const yamlText = await response.text();
    const parsedData = yaml.load(yamlText);
    const agentsArray = Object.values(parsedData.agents || {});
    setPlayerOptions(agentsArray);
  };

  const loadGameOptions = async () => {
    const url = '/game_settings.yaml';
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Failed to fetch YAML file: ${response.statusText}`);
    }
    const yamlText = await response.text();
    const parsedData = yaml.load(yamlText);
    setGameOptions(parsedData || {});
  };

  const makeAMove = (move) => {
    const result = game.move(move);
    if (result) {
      setGame(new Chess(game.fen()));
      setFenstring(game.fen());
      return result;
    } else {
      console.log("Invalid move:", move, "Current FEN:", game.fen());
      return null;
    }
  };

  useEffect(() => {
    loadPlayerOptions();
    loadGameOptions();
  }, []);

  return (
    <div className="App">
      <LeftPanel 
        playerOptions={playerOptions} 
        gameOptions={gameOptions} 
        gameStatus={gameStatus} 
      />
      <WebSocketHandler
        setGameStatus={setGameStatus}
        makeAMove={makeAMove}
        setConnectWebSocketFunc={(func) => setConnectWebSocketFunc(() => func)}
      />
      <MainSection
        game={game}
        makeAMove={makeAMove}
        moves={moves}
        fenstring={fenstring}
        setFenstring={setFenstring}
      />
    </div>
  );
}

export default App;
