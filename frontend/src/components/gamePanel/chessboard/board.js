import React, { useState } from "react";
import { Chessboard } from "react-chessboard";
import { Chess } from "chess.js"; // Import chess.js for game logic
import "./board.css";

function Board({game, makeAMove, setFenstring}) {
  // const [game, setGame] = useState(new Chess());

  // Handle piece drop
  function onDrop(sourceSquare, targetSquare) {
    const move = makeAMove({
      from: sourceSquare,
      to: targetSquare,
      promotion: "q", // Auto-promote to queen for simplicity
    });
    setFenstring(game.fen());

    // If the move is illegal
    if (move === null) return false;
    return true;
  }

  return (
    <div className="chessboard-container">
      <Chessboard 
        position={game.fen()} 
        onPieceDrop={onDrop} 
        boardOrientation="white" 
        boardWidth={500} 
      />
    </div>
  );
}

export default Board;
