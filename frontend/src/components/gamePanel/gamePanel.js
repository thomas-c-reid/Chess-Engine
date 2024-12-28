import React, { useState } from "react";
import Board from "./chessboard/board";
import PlayerPanel from "./playerPanel/playerPanel.js";
import FenstringBox from "./fenstringBox/fenstringBox.js";
import "./gamePanel.css";
import PlayerInfo from "./playerPanel/playerInformation/PlayerInfo.js";

function MainSection({whiteMoves, blackMoves, makeAMove, game, fenstring, setFenstring}) {

  return (
    <div className="game-panel">
      <div className="board-section">
        <PlayerPanel moves={whiteMoves}/>
        <Board game={game} makeAMove={makeAMove} setFenstring={setFenstring}/>
        <PlayerPanel moves={blackMoves}/>
      </div>

      <div className="lower-section">
        <FenstringBox fenstring={fenstring}/>
      </div>
    </div>
  );
}

export default MainSection;
