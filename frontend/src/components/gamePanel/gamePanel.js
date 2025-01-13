import React, { useState } from "react";
import Board from "./chessboard/board";
import PlayerPanel from "./playerPanel/playerPanel.js";
import FenstringBox from "./fenstringBox/fenstringBox.js";
import "./gamePanel.css";

function MainSection({whiteMoves, blackMoves, makeAMove, game, fenstring, playerData, takenPieces, activePlayer}) {

  console.log('WOWOWOWOWOWOWO')
  console.log(playerData)
  console.log('WOWOWOWOWOWOWO')

  return (
    <div className="game-panel">
      <div className="board-section">
        <PlayerPanel moves={whiteMoves} playerData={playerData} name='White' takenPieces={takenPieces} isActive={activePlayer === 'White'}/>
        <Board game={game} makeAMove={makeAMove} />
        <PlayerPanel moves={blackMoves} playerData={playerData} name='Black' takenPieces={takenPieces} isActive={activePlayer === 'Black'}/>
      </div>

      <div className="lower-section">
        <FenstringBox fenstring={fenstring}/>
      </div>
    </div>
  );
}

export default MainSection;
