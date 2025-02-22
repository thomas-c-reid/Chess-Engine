import React, {useState, useEffect} from "react";
import { Chessboard } from "react-chessboard";
import { Chess } from "chess.js";
import './css/board.css'


const Board = ({latest_move, setLatestMove, starting_fen, isBoardEnabled, setIsBoardEnabled, socket}) => {

    const [game, setGame] = useState(new Chess());

    function onDrop(sourceSquare, targetSquare) {

        if (!isBoardEnabled) return false;

        if (!socket || !socket.emit) {
            console.error("Socket not connected");
            return false;
        }

        const move = {
          from: sourceSquare,
          to: targetSquare,
          promotion: "q", // Auto-promote to queen for simplicity
        };
    
        if (move === null) return false;

        console.log("Move made:", move);
        setLatestMove(move);

        console.log('socket', socket);
        console.log('socket.emit', socket.emit);

        socket.emit("new_move", { move }, (ack) => {
            console.log("Server acknowledged move:", ack);
        });
        setIsBoardEnabled(false);
      }

    useEffect(() => {
        if (starting_fen) {
            console.log('In board useEffect - starting_fen:', starting_fen);
            const temp_game = new Chess();
            temp_game.load(starting_fen);
            setGame(temp_game);
        }
    }, [starting_fen])

    useEffect(() => {
        if (latest_move) {
            setGame((prevGame) => {
                const newGame = new Chess(prevGame.fen());  // Copy previous state
                
                console.log("Game before move:", newGame.fen());
                console.log("Attempting move:", latest_move);

                try {
                    newGame.move(latest_move);
                } catch (error) {
                    console.error("Error making move:", error);
                    return prevGame;
                }
    
                return newGame;
            });
        }
    }, [latest_move]);

    return (
        <div className="chessboard-container">
            <Chessboard boardWidth={450} position={game.fen()} onPieceDrop={onDrop}></Chessboard>
        </div>
    )
}

export default Board;