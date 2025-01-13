import yaml from 'js-yaml';

export const loadPlayerOptions = async (setPlayerOptions) => {
    const url = '/agent_info.yaml';
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Failed to fetch YAML file: ${response.statusText}`);
    }
    const yamlText = await response.text();
    const parsedData = yaml.load(yamlText);
    const agentsArray = Object.values(parsedData.agents || {});
    setPlayerOptions(agentsArray);
  };

export const loadGameOptions = async (setGameOptions) => {
    const url = '/game_settings.yaml';
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Failed to fetch YAML file: ${response.statusText}`);
    }
    const yamlText = await response.text();
    const parsedData = yaml.load(yamlText);
    setGameOptions(parsedData || {});
  };

export const loadPlayerData = async (setPlayerData, playerOneName, playerTwoName, game_info) => { 
    const url = '/agent_info.yaml';

    console.log('Loading player data...');
    try {
        // Fetch and parse the YAML file
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Failed to fetch YAML file: ${response.statusText}`);
        }

        const yamlText = await response.text();
        const parsedData = yaml.load(yamlText);

        console.log('Parsed Data:', parsedData);

        // Default player data
        const playerData = [
            { colour: 'White', name: null, bio: null, photo: null },
            { colour: 'Black', name: null, bio: null, photo: null },
        ];

        // Helper function to find player info
        const findPlayerInfo = (name) => {
            const agents = parsedData.agents || {};
            return agents[name] || null;
        };

        // Determine which players are white and black from game_info
        const whitePlayerName = game_info.white;
        const blackPlayerName = game_info.black;

        // Fetch player info for white
        const whitePlayerInfo = findPlayerInfo(whitePlayerName);
        if (whitePlayerInfo) {
            playerData[0] = {
                colour: 'White',
                name: whitePlayerInfo.name,
                bio: whitePlayerInfo.bio,
                photo: whitePlayerInfo.img_url || null,
                inputType: whitePlayerInfo.input_type || null,
            };
        }

        // Fetch player info for black
        const blackPlayerInfo = findPlayerInfo(blackPlayerName);
        if (blackPlayerInfo) {
            playerData[1] = {
                colour: 'Black',
                name: blackPlayerInfo.name,
                bio: blackPlayerInfo.bio,
                photo: blackPlayerInfo.img_url || null,
                inputType: blackPlayerInfo.input_type || null,
            };
        }

        // Update the state with the player data
        console.log('PlayerData:', playerData);
        setPlayerData(playerData);
    } catch (err) {
        console.error('Error loading player data:', err);
    }
};
