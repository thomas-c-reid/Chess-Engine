import React, { useState, useEffect, useRef } from "react";
import { io } from "socket.io-client";
import {loadPlayerInformation} from '../utils/loadGameInformation'
import useChesStore from "../store/chessStore";

const useWebSocket = ({setSocket}) => {

  const {setPlayers, setMoves, setPieces, setTime, setTimerState, setPlayerTurn, setLatestMove, setIsBoardEnabled, connectionState, setGameFen, time} = useChesStore();

  const socketRef = useRef(null);
  const websocketUrl = "http://localhost:5000";

  useEffect(() => {
    if (connectionState === 'READY') {
        connectToWebSocket();
        console.log('CONNECTING TO WEBSOCKET')
    }
  }, [connectionState]);

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
    })

    socket.on("new_game", async (game_information) => {

      try {
        const playerData = await loadPlayerInformation(game_information.white, game_information.black); // Await the Promise
        setPlayers(playerData);
      } catch (error) {
          console.error("Error loading player information:", error);
      }

      setGameFen(game_information.starting_fen);

      const timeMapping = {
        '1min': '1:00',
        '2min': '2:00',
        '5min': '5:00',
        '10min': '10:00'
      }
      const defaultTime = timeMapping[game_information.game_length] || '10:00';

      setTime({white: defaultTime, black: defaultTime});
      setTimerState('running');
    })

    socket.on("new_move", (moveWrapper) => {
      try {
        const moveString = moveWrapper.move;
        const jsonString = moveString.replace(/'/g, '"');
        const moveData = JSON.parse(jsonString);
        console.log('Move Received:', moveData);

        setLatestMove(moveData.move);

        setMoves(prevMoves => {
          const player = moveData.player.toLowerCase();
          const formattedMove = {
            move: moveData.move.to,
            time: moveData.time_taken || '00:00'
          }

          return {
            ...prevMoves,
            [player]: [...(prevMoves[player] || []), formattedMove]
          }

        });

        setPieces(moveData.taken_pieces);
        setPlayerTurn(moveData.player.toLowerCase());
        setIsBoardEnabled(true);


      } catch (error) {
        console.error('Error parsing move:', error)
        console.error('Raw move data:', moveWrapper)
      }
    })

    socket.on("game_over", () => {
      console.log('GAME FINISH')
    })

}};

export default useWebSocket;