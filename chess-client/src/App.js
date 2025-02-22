import { Chess } from 'chess.js';
import './App.css';
import Navbar from './components/navbar';
import Screen from './components/screen';
import WebSocketHandler from './services/websocketHandler';
import React, {useState} from 'react';

function App() {

  const [socket, setSocket] = useState(null);

  const [connectionState, setConnectionState] = useState('INIT');
  const [isFullScreen, setIsFullScreen] = useState(false);

  const [players, setPlayers] = useState({
    white: {name: 'White Player 1', description: 'Player 1 description'}, 
    black: {name: 'Black Player 2', description: 'Player 2 description'}
  });

  const [moves, setMoves] = useState({
    // white: [{move: 'e4', time: '2:41'}, {move: 'd5', time: '2:41'}],
    // black: [{move: 'e4', time: '2:41'}, {move: 'd5', time: '2:41'}]
    white: [],
    black: []
  });
  
  const [pieces, setPieces] = useState({
    white: [{queen: 0}, {rook: 0}, {bishop: 0}, {knight: 0}, {pawn: 0}],
    black: [{queen: 0}, {rook: 0}, {bishop: 0}, {knight: 0}, {pawn: 0}],
  });

  const [timerState, setTimerState] = useState('disabled'); // disabled, running, paused
  const [time, setTime] = useState({
    white: 300,
    black: 300
  });

  const [playerTurn, setPlayerTurn] = useState('None');
  const [latest_move, setLatestMove] = useState(null);
  const [starting_fen, setStartingFen] = useState(null);

  const [isBoardEnabled, setIsBoardEnabled] = useState(false);

  return (
    <div className={`App ${isFullScreen ? "minimised" : ""}`}>
        <WebSocketHandler setSocket={setSocket} connectionState={connectionState} setPlayers={setPlayers} setMoves={setMoves} setPieces={setPieces} setTime={setTime} setTimerState={setTimerState} setPlayerTurn={setPlayerTurn} setLatestMove={setLatestMove} setStartingFen={setStartingFen} setIsBoardEnabled={setIsBoardEnabled}/>
        <Navbar setConnectionState={setConnectionState} setIsFullScreen={setIsFullScreen}/>
        <Screen players={players} moves={moves} pieces={pieces} time={time} timerState={timerState} setTimerState={setTimerState} playerTurn={playerTurn} latest_move={latest_move} setLatestMove={setLatestMove} starting_fen={starting_fen} isBoardEnabled={isBoardEnabled} setIsBoardEnabled={setIsBoardEnabled} socket={socket}/>
    </div>
  );
}

export default App;
