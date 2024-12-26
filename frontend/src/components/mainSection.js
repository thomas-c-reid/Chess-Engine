import React, { useState } from "react";
import Board from "./board";
import FenStringBox from "./fenstringBox";
import PlayerInfo from "./PlayerInfo";
import Timer from "./timer";
import "../css/mainSection.css";

function MainSection({moves, makeAMove, game, fenstring, setFenstring}) {

  return (
    <div className="main-section">

      {/* Main Board */}
      <div className="board-section">
        <Board game={game} makeAMove={makeAMove} setFenstring={setFenstring}/>
      </div>
      
      {/* Player Info */}
      <div className="player-section player-one">
        <PlayerInfo playerName="Player One" />
      </div>
      <div className="timer-section player-one-timer">
        <Timer initialTime={300} />
      </div>
      <div className="player-section player-two">
        <PlayerInfo playerName="Player Two" />
      </div>
      <div className="player-two-timer">
        <Timer initialTime={300} />
      </div>

    {/* FEN String Box */}
    <div className="fen-box-section">
      <FenStringBox fenstring={fenstring}/>
    </div>
    </div>
  );
}

export default MainSection;
