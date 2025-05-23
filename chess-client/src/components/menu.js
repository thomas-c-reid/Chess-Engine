import React from 'react';
import {useState, useEffect, useRef} from 'react';
import "./css/menu.css"
import yaml from 'js-yaml';
import useChesStore from '../store/chessStore';
import { useWebSocket } from '../services/webSocketContext';

const Menu = () => {

    const {sendMessage} = useWebSocket();

    const {setPlayerTurn, setPlayers, setConnectionState, timeEnum, setTime, setTimerState} = useChesStore();
    const [selectedPlayerOne, setSelectedPlayerOne] = useState('RandomAgent');
    const [selectedPlayerTwo, setSelectedPlayerTwo] = useState('RandomAgent');
    const [selectedTimeOption, setSelectedTimeOption] = useState('');
    const [selectedStartOption, setSelectedStartOption] = useState('');
    const [selectedFenString, setSelectedFenString] = useState("")

    const [gameOptions, setGameOptions] = useState({});
    const [playerOptions, setPlayerOptions] = useState([]);

    // FUNCTION TO LOAD PLAYER NAMES FOR DROPDOWN
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
        console.warn(agentsArray)
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

    const load_player_from_name = (name) => {
        console.log(name)
        for (let i = 0; i < playerOptions.length; i++) {
            let temp = playerOptions[i]
            if (temp.name === name) {
                return temp
            }
        }
        return 0
    }

    const handleStartGame = async () => {

        const getRandomStart = () => (Math.random() < 0.5 ? 'P1' : 'P2');

        if (selectedStartOption === 'random') {
            setSelectedStartOption(getRandomStart());
        } else {
            console.log('not random bro')
        }

        if (!selectedFenString) {
            switch (selectedStartOption){
                case 'P1':
                    setPlayers({white: load_player_from_name(selectedPlayerOne), black: load_player_from_name(selectedPlayerTwo)});
                    break;
                    case 'P2':
                    setPlayers({white: load_player_from_name(selectedPlayerTwo), black: load_player_from_name(selectedPlayerOne)});
                    break;
                default:
                    console.error(`${selectedStartOption} is starting`)
                    break;
                }
        } else {
            // implement logic to figure out which player should start
        }

        const game_request_data = {
            selected_player_names: [selectedPlayerOne, selectedPlayerTwo],
            starts: selectedStartOption === 'random' ? getRandomStart() : selectedStartOption,
            game_length: selectedTimeOption,
            starting_fen: selectedFenString
        }
        console.log(game_request_data)
        sendMessage(JSON.stringify({'type': 'new_game', 'game_request': game_request_data}))

        setConnectionState('READY')
        setPlayerTurn('black')

        const selectedTime = timeEnum[selectedTimeOption];
        setTime({
        white: selectedTime,
        black: selectedTime
        });
        setTimerState('running')
        console.log()
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
                    {playerOptions.length > 0 ? (
                            playerOptions.map((agent, index) => (
                                <option key={index} value={agent.name}>
                                    {agent.name}
                                </option>
                            ))
                        ) : (
                            <option value="incorrectly loaded agents"></option>
                        )}
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
                <button className={`start-button`}
                onClick={handleStartGame}>
                    Start Match
                </button>
            </div>
        </div>
    )
}

export default Menu;