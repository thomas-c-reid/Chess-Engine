import React from 'react';
import {useState, useEffect, useRef} from 'react';
import "./css/menu.css"
import yaml from 'js-yaml';
import { io } from "socket.io-client";
import {postStartGame} from '../services/apiHandler';


const Menu = ({setConnectionState}) => {
    const [selectedPlayerOne, setSelectedPlayerOne] = useState('');
    const [selectedPlayerTwo, setSelectedPlayerTwo] = useState('');
    const [selectedTimeOption, setSelectedTimeOption] = useState('');
    const [selectedStartOption, setSelectedStartOption] = useState('');
    const [selectedFenString, setSelectedFenString] = useState("")

    const [isStartDisabled, setIsStartDisabled] = useState(true);
    const [gameOptions, setGameOptions] = useState({});
    const [playerOptions, setPlayerOptions] = useState([]);
    const socketRef = useRef(null);

    const loadGameData = async (setGameOptions, setPlayerOptions) => {
        // 1. Load agent options
        const agents_url = '/agent_info.yaml';
        const agents_response = await fetch(agents_url);
        if (!agents_response.ok){
            throw new Error('Failed to fetch YAML file: agent info')
        }
        const agentsYamlText = await agents_response.text();
        const agentsParsedData = yaml.load(agentsYamlText);
        const agentsArray = Object.values(agentsParsedData.agents || {})
        setPlayerOptions(agentsArray)
        
        // 2. Load game settings
        const settings_url = '/game_settings.yaml';
        const response = await fetch(settings_url);
        if (!response.ok){
            throw new Error('Failed to fetch YAML file: settings')
        }
        const yamlText = await response.text();
        const parsedData = yaml.load(yamlText);
        setGameOptions(parsedData || {})
    }

    const handleStartGame = async () => {

        if (!socketRef.current) {
            socketRef.current = io("http://localhost:5000")
        }

        socketRef.current.emit("new_game", {
            selected_player_names: [selectedPlayerOne, selectedPlayerTwo],
            starts: selectedStartOption,
            game_length: selectedTimeOption,
            starting_fen: selectedFenString
        })

        console.log('JUST EMIT WEBSOCKET START_GAME CONNECT')

        setConnectionState('READY')

        // const payload = {
        //     selected_player_names: [selectedPlayerOne, selectedPlayerTwo],
        //     starts: selectedStartOption,
        //     game_length: selectedTimeOption,
        //     starting_fen: selectedFenString
        // };

        // try{
        //     await postStartGame(payload, setConnectionState)
        // } catch (err) {
        //     console.log(err)
        // }
    }

    useEffect(() => {
        loadGameData(setGameOptions, setPlayerOptions);
    }, []);

    return(
        <div className='menu'>
            <div className='dropdown-group'>
                <label className="dropdown-label">Player One:</label>
                <select className="player-choice-dropdown"
                id="playerOne"
                value={selectedPlayerOne}
                onChange={(e) => setSelectedPlayerOne(e.target.value)}>
                {playerOptions.length > 0 ? (
                    playerOptions.map((agent, index) => (
                        <option key={index} value={agent.name}>
                            {agent.name}
                        </option>
                    ))
                ) : (
                    <option value="error"></option>
                )}
               
                </select>
            </div>

            <div className='dropdown-group'>
                <label>Player Two</label>
                <select
                id="playerTwo"
                className="player-choice-dropdown"
                value={selectedPlayerTwo}
                onChange={(e) => setSelectedPlayerTwo(e.target.value)}>
                    {
                        playerOptions.length > 0 ? (
                            playerOptions.map((agent, idx) => (
                                <option key={idx} value={agent.name}>
                                    {agent.name}
                                </option>
                            ))
                        ) : (
                            <option value="incorrectly loaded agents"></option>
                        )

                    }
                </select>
            </div>

            <div className="tab-group">
                <label>Select Game Time:</label>
                <div className="tab-container">
                    {
                        gameOptions.time_options?.length > 0 ? (
                            gameOptions.time_options.map((timeOption, index) => (
                                <div
                                key={index}
                                className={`tab-item ${selectedTimeOption === timeOption ? "active" : ""}`}
                                onClick={() => setSelectedTimeOption(timeOption)}>
                                     {timeOption.replace(/_/g, " ")}
                                </div>
                            ))
                        ) : (
                            <span>Loading...</span>
                        )
                    }
                </div>
            </div>

            <div className="tab-group">
                <label>Select Who Starts: </label>
                <div className='tab-container'>
                    {gameOptions.starting_options?.length > 0 ? (
                        gameOptions.starting_options.map((option, index) => (
                            <div
                            key={index}
                            className={`tab-item ${selectedStartOption === option ? "active" : ""}`}
                            onClick={() => setSelectedStartOption(option)}>
                                {option.replace(/_/g, " ")}
                            </div>
                        )) 
                    ) : (
                        <span>loading</span>
                    )}
                </div>
            </div>

            <div className="input-group">
                <label className='input-label'>Custom Fen Position:</label>
                <input className="fen-input" value={selectedFenString} onChange={(e) => setSelectedFenString(e.target.value)}></input>
            </div>

            <div className="button-group">
                <button className={`start-button ${isStartDisabled ? "active" : ""}`}
                onClick={handleStartGame}>
                    Start Match
                </button>
            </div>
        </div>
    )
}

export default Menu;