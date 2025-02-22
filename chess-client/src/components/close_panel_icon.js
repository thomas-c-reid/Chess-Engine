import React from 'react';
import './css/close_panel_icon.css'

const ClosePanelIcon = ({setIsFullScreen}) => {
    return (
        <button className="close-panel" onClick={() => (setIsFullScreen(true))}>
            X
        </button>
        //
        //
      
        // <button className="" onClick={() => (setIsFullScreen(true))}>
            // {/* <img src="icons/left-align.png" alt="close panel"/> */}
        // {/* </button> */}
    );
}

export default ClosePanelIcon;