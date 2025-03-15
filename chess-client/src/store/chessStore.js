import { create } from 'zustand';

const useChesStore = create((set) => ({

    players: {
        white: {name: 'White Player 1', description: 'Player 1 description'}, 
        black: {name: 'Black Player 2', description: 'Player 2 description'}
      },

    moves: {
        white: [],
        black: []
    },

    pieces: {
        white: [{queen: 0}, {rook: 0}, {bishop: 0}, {knight: 0}, {pawn: 0}],
        black: [{queen: 0}, {rook: 0}, {bishop: 0}, {knight: 0}, {pawn: 0}],
    },

    timerState: 'disabled',
    time: {
        white: 300,
        black: 300
    },
    playerTurn: 'None',
    latest_move: null,
    starting_fen: null,
    isBoardEnabled: false,

    setPlayers: (players) => set({players}),
    setMoves: (moves) => set({moves}),
    setPieces: (pieces) => set({pieces}),
    setTimerState: (timerState) => set({timerState}),
    setTime: (time) => set({time}),
    setPlayerTurn: (playerTurn) => set({playerTurn}),
    setLatestMove: (latest_move) => set({latest_move}),
    setStartingFen: (starting_fen) => set({starting_fen}),
    setIsBoardEnabled: (isBoardEnabled) => set({isBoardEnabled}),

}));
