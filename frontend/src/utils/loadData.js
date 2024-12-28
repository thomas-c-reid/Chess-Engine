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

