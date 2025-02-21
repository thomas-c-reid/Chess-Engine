import React from 'react';
import './css/close_panel_icon.css'

const ClosePanelIcon = ({setIsFullScreen}) => {
    return (
        <button className="close-panel" onClick={() => (setIsFullScreen(true))}>X</button>
    );
}

export default ClosePanelIcon;