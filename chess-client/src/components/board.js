import React, {useState, useEffect} from "react";
import { Chessboard } from "react-chessboard";
import { Chess } from "chess.js";
import './css/board.css'


const Board = ({latest_move, starting_fen}) => {

    const [game, setGame] = useState(new Chess());

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
    
                const move = newGame.move(latest_move);
                if (!move) {
                    console.error("❌ Invalid move detected:", latest_move);
                    return prevGame;  // Don't update state if the move is invalid
                }
    
                return newGame;
            });
        }
    }, [latest_move]);
    




    return (
        <div className="chessboard-container">
            <Chessboard boardWidth={450} position={game.fen()}></Chessboard>
        </div>
    )
}

export default Board;