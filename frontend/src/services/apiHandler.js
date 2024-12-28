export const postStartGame = async ({payload, connectToWebSocket, setGameStatus}) => {
    try {
        // POST to Flask API to start the game
        const response = await fetch("http://localhost:5000/api/start-match", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        if (response['status'] == 200) {
            setGameStatus('Connection established')
        } else {
            setGameStatus('Connection failed', response['status'])
        }

        if (connectToWebSocket) {
            console.log('ATTEMPING TO CONNECT TO WEBSOCKET', connectToWebSocket)
            await connectToWebSocket();
            console.log('?????')
        } else {
            console.error('No Websocket connection function provided');
        }

    } catch (err) {
        console.error("Error starting game:", err);
        setGameStatus("Failed to start game.");
    }
}