import { create } from 'zustand';
import { Chess } from "chess.js";

const useChesStore = create((set) => ({

    players: {
        white: {name: 'White Player 1', description: 'Player 1 description'}, 
        black: {name: 'Black Player 2', description: 'Player 2 yo yo yo'}
      },

    moves: {
        white: [],
        black: []
    },

    pieces: {
        white: [{queen: 0}, {rook: 0}, {bishop: 0}, {knight: 0}, {pawn: 0}],
        black: [{queen: 0}, {rook: 0}, {bishop: 0}, {knight: 0}, {pawn: 0}],
    },

    time: {
        white: 300,
        black: 300
    },
    timeEnum: {
        "1min": 60,
        "2min": 120,
        "5min": 300,
        "10min": 600
    },
    timerState: 'disabled',
    playerTurn: 'None',
    latest_move: null,
    starting_fen: null,
    isBoardEnabled: false,
    connectionState: 'INIT',
    gameFen: new Chess().fen(),

    setPlayers: (players) => set({players}),
    setMoves: (moves) => set({moves}),
    setPieces: (pieces) => set({pieces}),
    setTime: (time) => set({time}),
    setTimerState: (timerState) => set({timerState}),
    setPlayerTurn: (playerTurn) => set({playerTurn}),
    setLatestMove: (latest_move) => set({latest_move}),
    setIsBoardEnabled: (isBoardEnabled) => set({isBoardEnabled}),
    setConnectionState: (connectionState) => set({connectionState}),
    setGameFen: (gameFen) => set({gameFen}),

    websocketUrl: "http://localhost:5000",
}));

export default useChesStore;