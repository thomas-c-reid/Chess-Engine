import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSkull, faPause, faRotateRight, faCopy } from "@fortawesome/free-solid-svg-icons";

export function ControlButtons({setTimerState}) {

    const pauseGame = () => {
        setTimerState('paused');
    }
    return (
        <>
            {/* <button className='game-control-button pause' onClick={pauseGame}>
                <FontAwesomeIcon icon={faPause} />
            </button> */}
            <button className='game-control-button kill'>
                <FontAwesomeIcon icon={faSkull} />
            </button>
            <button className='game-control-button restart'>
                <FontAwesomeIcon icon={faRotateRight} />
            </button>
            <button className='game-control-button fen'>
                <FontAwesomeIcon icon={faCopy} />
            </button> 
            <label className='game-control-button rating'>
                +3
            </label>
        </>
    );
}