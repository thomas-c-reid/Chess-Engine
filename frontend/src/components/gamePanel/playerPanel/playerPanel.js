import PlayerInfo from "./playerInformation/PlayerInfo.js";
import Timer from "./timer/timer.js";
import Moves from "./moves/moves.js";
import TakenPieces from "./takenPieces/takenPieces.js";
import "./playerPanel.css";

function PlayerPanel ({moves, playerData, name, takenPieces, isActive}) {
    return (
        <div className="player-panel-container">
            <PlayerInfo playerData={playerData} name={name}/>
            <Timer initialTime={300} isActive={isActive}/>
            <Moves moves={moves}/>
            <TakenPieces takenPieces={takenPieces}/>

        </div>
    )
}
export default PlayerPanel;