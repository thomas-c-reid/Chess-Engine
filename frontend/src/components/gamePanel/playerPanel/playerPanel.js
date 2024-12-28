import PlayerInfo from "./playerInformation/PlayerInfo.js";
import Timer from "./timer/timer.js";
import Moves from "./moves/moves.js";
import "./playerPanel.css";

function PlayerPanel ({moves}) {
    return (
        <div className="player-panel-container">
            <PlayerInfo playerName="Player One" />
            <Timer initialTime={300}/>
            <Moves moves={moves}/>
        </div>
    )
}
export default PlayerPanel;