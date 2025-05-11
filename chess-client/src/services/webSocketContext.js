import { createContext, useContext, useEffect, useRef } from "react";
import useChesStore from "../store/chessStore";

const WebSocketContext = createContext(null);

export const WebSocketProvider = ({children}) => {
    
    const ws = useRef(null)
    const {setPlayers, setMoves, setPieces, setTime, setTimerState, setPlayerTurn, setLatestMove, setIsBoardEnabled, connectionState, setGameFen, time, websocketUrl} = useChesStore()

    const handleMessage = (message_data) => {
      console.log('handling message...')
      console.log(message_data)
      console.log('.')
    }

    useEffect(() => {
        ws.current = new WebSocket(websocketUrl);
      
        ws.current.onopen = () => {
          console.log('CONNECTED TO WEBSOCKET SERVICE - USING CONTEXT');
        };
      
        ws.current.onmessage = async (event) => {
          try {
            console.log('CAUGHT DATA!', event);
            const mesage_data = JSON.parse(event.data)

            setGameFen(mesage_data.fen)
          } catch (error) {
            console.log("WebSocket message error", error);
          }
        };
      
        return () => {
          ws.current?.close();
        };
      }, [websocketUrl]);

      const sendMessage = (data) => {
        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
            const message = JSON.stringify({data});
            ws.current.send(message);
        } else {
            console.log('websocket is not open. Cannot send message')
        }
      }
    
    return (
        <WebSocketContext.Provider value={{sendMessage}}>
            {children}
        </WebSocketContext.Provider>
    )
}

export const useWebSocket = () => useContext(WebSocketContext);