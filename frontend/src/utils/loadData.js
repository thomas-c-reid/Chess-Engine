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

export const loadPlayerData = async (setPlayerData, playerOneName, playerTwoName) => { 
    console.log('playerTwoName:', playerTwoName); 
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
  
      // Search for playerOne info
      const playerOneInfo = findPlayerInfo(playerOneName);
      if (playerOneInfo) {
        playerData[0] = {
          colour: 'White',
          name: playerOneInfo.name,
          bio: playerOneInfo.bio,
          photo: playerOneInfo.img_url || null,
          inputType: playerOneInfo.input_type || null,
        };
      }
  
      // Search for playerTwo info
      const playerTwoInfo = findPlayerInfo(playerTwoName);
      if (playerTwoInfo) {
        playerData[1] = {
          colour: 'Black',
          name: playerTwoInfo.name,
          bio: playerTwoInfo.bio,
          photo: playerTwoInfo.img_url || null,
          inputType: playerOneInfo.input_type || null,
        };
      }
  
      // Update the state with the player data
      console.log('PlayerData:', playerData);
      setPlayerData(playerData);
    } catch (err) {
      console.error('Error loading player data:', err);
    }
  };
  