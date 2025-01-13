import React, { useState, useEffect, useRef } from "react";
const { io } = require("socket.io-client");

function WebSocketHandler({ setGameStatus, makeAMove, setConnectWebSocketFunc, loadPlayerData, setPlayerData }) {
  const [isConnected, setIsConnected] = useState(false);
  const socketRef = useRef(null);
  const websocketUrl = "http://localhost:5000"

  const connectToWebSocket = () => {
    if (isConnected || socketRef.current) {
      console.log("Already connected to websocket");
      return;
    }

    const socket = io(websocketUrl);
    socketRef.current = socket;

    socket.on("connect", () => {
      setGameStatus("Connected to websocket");
      console.log('CONNECTED TO WEBSOCKET ON URL:', websocketUrl)
      setIsConnected(true);
    });

    socket.on("new_game", (game_info) => {
      const playerOne = document.getElementById("playerOne").value;
      const playerTwo = document.getElementById("playerTwo").value;

      console.log('#######')
      console.log(game_info)
      console.log(playerOne)
      console.log(playerTwo)
      console.log('#######')

      loadPlayerData(setPlayerData, playerOne, playerTwo, game_info);

    })

    socket.on("new_move", (data) => {
      const jsonString = data["move"].replace(/'/g, '"');
      const parsedData = JSON.parse(jsonString);

      // TODO: Check if move has 'start' flag so we know to begin a match
      makeAMove(parsedData);
    });

    socket.on("disconnect", () => {
      setIsConnected(false);
      setGameStatus("Disconnected from websocket");
    });
  };

  const disconnectFromWebSocket = () => {
    if (socketRef.current) {
      socketRef.current.disconnect();
      socketRef.current = null;
      setIsConnected(false);
      setGameStatus("Disconnected from websocket");
    }
  };

  useEffect(() => {
    if (setConnectWebSocketFunc) {
      setConnectWebSocketFunc(connectToWebSocket);
    }
  
    return () => {
      if (socketRef.current) {
        socketRef.current.disconnect();
      }
    };
  }, []);
  
  return null;
}

export default WebSocketHandler;
