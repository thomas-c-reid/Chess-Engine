import React, { useState, useEffect } from "react";
import { Chessboard } from "react-chessboard";
import { Chess } from "chess.js";
import './css/board.css';
import useChessStore from '../store/chessStore';

const Board = ({ socket }) => {
    // Use chess store to manage the game state
    const {
        gameFen,
        latest_move,
        setLatestMove,
        setPlayerTurn,
        setMoves,
        isBoardEnabled,
        setIsBoardEnabled
    } = useChessStore();

    const [game, setGame] = useState(new Chess());

    function onDrop(sourceSquare, targetSquare) {
        if (!isBoardEnabled) return false;

        if (!socket || !socket.emit) {
            console.error("Socket not connected");
            return false;
        }

        const move = {
            from: sourceSquare,
            to: targetSquare
        };

        if (move === null) return false;

        setMoves(prevMoves => {
            const player = game.turn() === "w" ? "white" : "black";
            const formattedMove = {
                move: latest_move.to,
                time: '00:00'
            };

            return {
                ...prevMoves,
                [player]: [...(prevMoves[player] || []), formattedMove]
            };
        });

        console.log("Move made:", move);
        setLatestMove(move);

        socket.emit("new_move", { move }, (ack) => {
            console.log("Server acknowledged move:", ack);
        });
        setIsBoardEnabled(false);
    }

    useEffect(() => {
        if (gameFen) {
            console.log('In board useEffect - starting_fen:', gameFen);
            const temp_game = new Chess();
            temp_game.load(gameFen);
            setGame(temp_game); // Set the initial game state from FEN in the store
        }
    }, [gameFen]);

    useEffect(() => {
        if (latest_move) {
    
            const temp_game = new Chess(game.fen());
            console.log('latest_move updated', latest_move);
    
            try {
                const move_result = temp_game.move({
                    from: latest_move.from,
                    to: latest_move.to,
                    promotion: latest_move.promotion || 'q'
                });
                setGame(temp_game);
    
                const playerTurn = temp_game.turn() === "w" ? "black" : "white";
                setPlayerTurn(playerTurn);
            } catch (error) {
                console.error("Error making move:", error);
            }
        }
    }, [latest_move]);
    
    if (!game) {
        return <div>Loading...</div>; // Or any loading indicator
    }

    return (
        <div className="chessboard-container">
            <Chessboard 
                boardWidth={450} 
                position={game.fen()}
                onPieceDrop={onDrop} 
            />
        </div>
    );
};

export default Board;
