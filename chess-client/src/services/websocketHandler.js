import React, { useState, useEffect, useRef } from "react";
import { io } from "socket.io-client";
import { Chess } from "chess.js";
import {loadPlayerInformation} from '../utils/loadGameInformation'

function WebSocketHandler({setSocket, connectionState, setPlayers, setMoves, setPieces, setTime, setTimerState, setPlayerTurn, setLatestMove, setStartingFen, setIsBoardEnabled}) {
  const [isConnected, setIsConnected] = useState(false)
  const socketRef = useRef(null);
  const websocketUrl = "http://localhost:5000";

  const connectToWebSocket = () => {
    if (socketRef.current) {
        console.log("Already connected to websocket");
        return;
      }

    const socket = io(websocketUrl)
    socketRef.current = socket
    setSocket(socketRef.current)

    socket.on("connect", () => {
        console.log('CONNECTED TO WEBSOCKET ON URL:', websocketUrl)
        setIsConnected(true);
      });

    socket.on("new_game", async (game_information) => {
      console.log('Starting Game', game_information)

      // update player information
      try {
        const playerData = await loadPlayerInformation(game_information.white, game_information.black); // Await the Promise
        setPlayers(playerData); // Now it's resolved and can be used
      } catch (error) {
          console.error("Error loading player information:", error);
      }

      // update game state
      // const temp_chess = new Chess();
      // temp_chess.load(game_information.starting_fen);
      // setGame(temp_chess);
      setStartingFen(game_information.starting_fen);

      // update Time
      const timeMapping = {
        '1min': '1:00',
        '2min': '2:00',
        '5min': '5:00',
        '10min': '10:00'
      }
      const defaultTime = timeMapping[game_information.game_length] || '10:00';
      setTime({white: defaultTime, black: defaultTime});
      setTimerState('paused');
        
    });

    socket.on("new_move", (moveWrapper) => {
      try {

        console.log('New Move:', moveWrapper);
  
        // grab the move data from the moveWrapper and parse it to JSON
        const moveString = moveWrapper.move;
        const jsonString = moveString.replace(/'/g, '"');
        const moveData = JSON.parse(jsonString);

        setLatestMove(moveData.move);
        console.log('Set Latest Move:', moveData.move);

        // if white we want to update white moves list, else black
        setMoves(prevMoves => {

          const player = moveData.player.toLowerCase();

          const formattedMove = {
            move: moveData.move.to,
            time: '00:00'
          }

          return {
            ...prevMoves,
            [player]: [...(prevMoves[player] || []), formattedMove]
          }

        });

        setPieces(moveData.taken_pieces);

        setTimerState('running');
        console.log('Player Turn:', moveData.player.toLowerCase())
        setPlayerTurn(moveData.player.toLowerCase());

      } catch (error) {
        console.error('Error parsing move:', error);
        console.error('Raw move data:', moveWrapper);
      }
    });

    socket.on('request_move', () => {
      setIsBoardEnabled(true);
    });

    socket.on("game_over", () => {
        console.log('Game finished')
    })
  }

  useEffect(() => {
    if (connectionState === 'READY') {
        connectToWebSocket();
    }
  }, [connectionState]);

};

export default WebSocketHandler;