export const postStartGame = async (payload, setConnectionState) => {
    try {
        const response = await fetch("http://localhost:5000/api/start-match", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(payload)
        });
        console.log('response', response)

        // if connection contains some flag we connect to websocket
        if (1 === 1){
            setConnectionState('READY')
            return true
        }



    } catch (err){
        console.log('error posting data')
        console.log(err)
    }

}
