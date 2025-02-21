import React, {useState, useEffect} from 'react';
import './css/timer.css';

export function Timer({whiteTime, blackTime, timerState, playerTurn}) {

    const [whiteTimer, setWhiteTimer] = useState(whiteTime);
    const [blackTimer, setBlackTimer] = useState(blackTime);

    useEffect(() => {
        if (timerState === 'running') {
            const interval = setInterval(() => {
                console.log('Bang')
                if (playerTurn === 'white') {
                    setBlackTimer(prevTime => prevTime > 0 ? prevTime - 1 : 0);
                } else {
                    setWhiteTimer(prevTime => prevTime > 0 ? prevTime - 1 : 0);
                }
            }, 1000);
            return () => clearInterval(interval);
        }
    }, [playerTurn]);

    const formatTime = (time) => {
        const minutes = Math.floor(time / 60);
        const seconds = time % 60;
        return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    };

    return (
        <div className="player-timer-container">
            <div className="player-timer white">
                <label>{formatTime(whiteTimer)}</label>
            </div>
            <div className="player-timer black">
                <label>{formatTime(blackTimer)}</label>
            </div>
        </div>
    );
}