import React from "react";
import yaml from 'js-yaml';

export const loadPlayerInformation = async(whiteName, blackName) => {

    const base_response = {
        white: {name: 'White Player', description: 'Player 1 description'}, 
        black: {name: 'Black Player', description: 'Player 2 description'}
    };

    const url = './agent_info.yaml';
    const response = await fetch(url);

    if (!response.ok) {
          throw new Error(`Failed to fetch YAML file: ${response.statusText}`);
        }
    const yamlText = await response.text();
    const parsedData = yaml.load(yamlText);

    try {
        const whiteMan = Object.values(parsedData.agents).find(agent => agent.name === whiteName);
        base_response.white = {
            name: whiteMan.name,
            description: whiteMan.bio
        };
    } catch (err) {
        console.error('Error loading player information:', err);
    }

    try {
        const blackMan = Object.values(parsedData.agents).find(agent => agent.name === blackName);
        
        base_response.black = {
            name: blackMan.name,
            description: blackMan.bio
        };
    } catch (err) {
        console.error('Error loading player information:', err);
    }

    return base_response;
}