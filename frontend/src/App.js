// App.js

import './App.css';
import Board from './components/gamePanel/chessboard/board.js';
import WebSocketHandler from './services/websocketHandler.js';
import React, { useState, useEffect } from "react";
import { Chess } from 'chess.js';
import LeftPanel from './components/settingsPanel/leftPanel.js'
import MainSection from './components/gamePanel/gamePanel.js';
import { loadPlayerOptions, loadGameOptions } from './utils/loadData.js';

function App() {
  const [whiteMoves, setWhiteMoves] = useState([]);
  const [blackMoves, setBlackMoves] = useState([]);
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

  const makeAMove = (move) => {
    const moveString = `${move['move']['from']} -> ${move['move']['to']}`;

    const result = game.move(move['move']);
    if (move['player'] == 'White') {
      setWhiteMoves((prevWhiteMoves) => [...prevWhiteMoves, moveString])
    } else {
      setBlackMoves((prevBlackMoves) => [...prevBlackMoves, moveString]);
    }
    if (result) {
      setGame(new Chess(game.fen()));
      setFenstring(game.fen());
      return result;
    } else {
      console.log("Invalid move:", move, "Current FEN:", game.fen());
      return null;
    }
  }

  useEffect(() => {
    loadPlayerOptions(setPlayerOptions);
    loadGameOptions(setGameOptions);
  }, []);


  return (
    <div className="App">
      <LeftPanel 
        playerOptions={playerOptions} 
        gameOptions={gameOptions} 
        gameStatus={gameStatus} 
        connectToWebSocket={connectWebSocketFunc}
        setGameStatus={setGameStatus}
      />
      <WebSocketHandler
        setGameStatus={setGameStatus}
        makeAMove={makeAMove}
        setConnectWebSocketFunc={(func) => setConnectWebSocketFunc(() => func)}
        setGame={setGame}
        setFenstring={setFenstring}
      />
      <MainSection
        game={game}
        makeAMove={makeAMove}
        whiteMoves={whiteMoves}
        blackMoves={blackMoves}
        fenstring={fenstring}
        setFenstring={setFenstring}
      />
    </div>
  );
}

export default App;
