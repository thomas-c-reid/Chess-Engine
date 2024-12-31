// App.js

import './App.css';
import WebSocketHandler from './services/websocketHandler.js';
import React, { useState, useEffect } from "react";
import { Chess } from 'chess.js';
import LeftPanel from './components/settingsPanel/leftPanel.js'
import MainSection from './components/gamePanel/gamePanel.js';
import { loadPlayerOptions, loadGameOptions, loadPlayerData } from './utils/loadData.js';

function App() {
  const [whiteMoves, setWhiteMoves] = useState([]);
  const [blackMoves, setBlackMoves] = useState([]);
  const [game, setGame] = useState(new Chess());
  const [playerOptions, setPlayerOptions] = useState([]);
  const [gameOptions, setGameOptions] = useState([]);
  const [connectWebSocketFunc, setConnectWebSocketFunc] = useState(null);
  const [fenstring, setFenstring] = useState("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1");
  const [playerData, setPlayerData] = useState([
    {colour: 'White', name: null, bio: null, photo: null, inputType: null},
    {colour: 'Black', name: null, bio: null, photo: null, inputType: null}]);
  const [gameStatus, setGameStatus] = useState({
    apiConnected: false,
    websocketConnected: false,
    gameInProgress: false,
  });
  const [takenPieces, setTakenPieces] = useState([
    {piece: 'p', count: 0}, {piece: 'k', count: 0},
    {piece: 'b', count: 0}, {piece: 'r', count: 0},
    {piece: 'q', count: 0}]);
  
  const [activePlayer, setActivePlayer] = useState();
  const [isBoardInteractive, setIsBoardInteractive] = useState(false);
  
  const makeAMove = (move) => {
    // add moves to list
    const moveString = `${move['move']['from']} -> ${move['move']['to']}`;
    const result = game.move(move['move']);
    if (move['player'] == 'White') {
      setWhiteMoves((prevWhiteMoves) => [...prevWhiteMoves, moveString])
    } else {
      setBlackMoves((prevBlackMoves) => [...prevBlackMoves, moveString]);
    }

    if (result) {
      // set player chaged
      setActivePlayer(move['player'] === "White" ? "Black" : "White"); 

      const currentPlayerData = playerData.find(player => player.colour === move['player']);
      if (currentPlayerData && currentPlayerData.inputType === 'manual') {
        setIsBoardInteractive(true);
      } else {
        setIsBoardInteractive(false);
      }
      // should also be looking to check what input type the current player is, if manual, then we should be waiting for a move, 
      // if websocket, we should wait for new move to come in 

      // update game
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
        loadPlayerData={loadPlayerData}
        setPlayerData={setPlayerData}
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
        playerData={playerData}
        takenPieces={takenPieces}
        activePlayer={activePlayer}
      />
    </div>
  );
}

export default App;
