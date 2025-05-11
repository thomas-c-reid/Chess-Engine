import { Chess } from 'chess.js';
import './App.css';
import Navbar from './components/navbar';
import Screen from './components/screen';
import React, {useState} from 'react';
import { WebSocketProvider } from './services/webSocketContext';

function App() {

  const [isFullScreen, setIsFullScreen] = useState(false);

  return (
    <WebSocketProvider>
      <div className={`App ${isFullScreen ? "minimised" : ""}`}>
          <Navbar setIsFullScreen={setIsFullScreen}/>
          <Screen />
      </div>
    </WebSocketProvider>
  );
}

export default App;
