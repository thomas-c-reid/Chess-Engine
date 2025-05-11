import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSkull, faPause, faRotateRight, faCopy } from "@fortawesome/free-solid-svg-icons";
import useChesStore from "../store/chessStore";
import { Chess } from "chess.js";

export function ControlButtons({}) {

    const {setTime, setGame, setTimerState, gameFen} = useChesStore();
    const socket = null;

    const resetGame = () => {
        console.log('RESETTING GAME')

        if (!socket || !socket.emit) {
            console.error("Socket not connected");
            return false;
        }

        socket.emit("terminate_game", '', (ack) => {
            console.log("Server acknowledged move:", ack);
        });
        setTime({white: '00:00', black: '00:00'});
        setTimerState('disabled');
        setGame(new Chess());
    }

    const restartGame = () => {
        console.log('RESTARTING GAME')

        if (!socket || !socket.emit) {
            console.error("Socket not connected");
            return false;
        }
        
        socket.emit("restart_game", '', (ack) => {
            console.log("Server acknowledged move:", ack);
        });

        setTime({white: '00:00', black: '00:00'});
        setGame(new Chess());
    }

    const copyFen = () => {
        navigator.clipboard.writeText(gameFen);
    }

    return (
        <>
            <button className='game-control-button kill'>
                <FontAwesomeIcon icon={faSkull} onClick={resetGame}/>
            </button>
            <button className='game-control-button restart'>
                <FontAwesomeIcon icon={faRotateRight} onClick={restartGame}/>
            </button>
            <button className='game-control-button fen'>
                <FontAwesomeIcon icon={faCopy} onClick={copyFen}/>
            </button> 
            <label className='game-control-button rating'>
                +3
            </label>
        </>
    );
}