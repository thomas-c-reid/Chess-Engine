import { Chess } from 'chess.js';
import './App.css';
import Navbar from './components/navbar';
import Screen from './components/screen';
import useWebSocket from './services/useWebSocket';
import React, {useState} from 'react';

function App() {

  const [socket, setSocket] = useState(null);

  const [connectionState, setConnectionState] = useState('INIT');
  const [isFullScreen, setIsFullScreen] = useState(false);

  useWebSocket({setSocket});

  return (
    <div className={`App ${isFullScreen ? "minimised" : ""}`}>
        <Navbar setIsFullScreen={setIsFullScreen}/>
        <Screen socket={socket}/>
    </div>
  );
}

export default App;
