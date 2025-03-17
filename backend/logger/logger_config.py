import logging
import logging.config
import os
import yaml

class Logging:

    def __init__(self):
        config_dir = 'logger/logging_config.yaml'
        logs_dir = 'logger/logs'
        
        for filename in os.listdir(logs_dir):
            if not os.path.exists(logs_dir):
                os.makedirs(logs_dir)
            else:
                open(f'{logs_dir}/{filename}', 'w').close()
            
        if os.path.exists(config_dir):
            with open(config_dir, 'rt') as file:
                config = yaml.safe_load(file.read())
                logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=logging.INFO)
            
    def get_logger(self, name='gameplay'):
        return logging.getLogger(name)