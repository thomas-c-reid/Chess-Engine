import React, { useState, useEffect } from 'react';
import Board from './board';
import './css/screen.css'
import {ControlButtons} from './controlButtons';
import {PlayerCard} from './playerCard';
import './timer'
import { Timer } from './timer';
import { MovesContainer } from './movesContainer'; 

const Screen = ({players, moves, pieces, time, timerState, setTimerState, playerTurn, latest_move, starting_fen}) => {
    
    return (
        <div className='screen'>
            <div className='player-info'>

                {/* <PlayerCard className='player-card left' playerData={players.white}/> */}
                <PlayerCard 
                    // className='player-card left' 
                    className={`player-card left ${playerTurn === 'black' ? 'active' : 'inactive'}`}
                    playerData={players.white}/>

                <div>
                    <div className='player-timer-top-row'>
                        <Timer whiteTime={time.white} blackTime={time.black} timerState={timerState} playerTurn={playerTurn}/>
                    </div>

                    <div className="game-control-button-container">
                        <ControlButtons setTimerState={setTimerState} />
                    </div>
                </div>

                <PlayerCard 
                    // className='player-card right' 
                    className={`player-card right ${playerTurn === 'white' ? 'active' : 'inactive'}`}
                    playerData={players.black}/>

            </div>

            <div className="game-container">

                <MovesContainer moves={moves.white} pieces={pieces.white}/>

                <div className="board-contanier">
                    {/* <Board game={game} setGame={setGame}/> */}
                    <Board latest_move={latest_move} starting_fen={starting_fen}/>
                </div>
                <MovesContainer moves={moves.black} pieces={pieces.black}/>
            </div>
        </div>
    );
};

export default Screen;