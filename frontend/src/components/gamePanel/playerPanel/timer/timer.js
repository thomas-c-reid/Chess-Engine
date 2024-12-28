import React, { useState, useEffect } from 'react';
import './timer.css'

const Timer = ({ initialTime }) => {
    const [time, setTime] = useState(initialTime);
    const [isActive, setIsActive] = useState(false);

    useEffect(() => {
        let interval = null;
        if (isActive) {
            interval = setInterval(() => {
                setTime(prevTime => {
                    const minutes = Math.floor(prevTime / 60);
                    const seconds = prevTime % 60;
                    if (minutes === 0 && seconds === 0) {
                        clearInterval(interval);
                        return 0;
                    }
                    return prevTime - 1;
                });
            }, 1000);
        } else if (!isActive && time !== 0) {
            clearInterval(interval);
        }
        return () => clearInterval(interval);
    }, [isActive, time]);

    const formatTime = (time) => {
        const minutes = Math.floor(time / 60);
        const seconds = time % 60;
        return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    };

    return (
        <div className='timer-container'>
            <div>{formatTime(time)}</div>
            {/* <button onClick={() => setIsActive(!isActive)}>
                {isActive ? 'Pause' : 'Start'}
            </button> */}
        </div>
    );
};

export default Timer;