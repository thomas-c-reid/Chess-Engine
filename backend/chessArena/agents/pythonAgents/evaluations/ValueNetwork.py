from dotenv import load_dotenv
from pathlib import Path
from logger.logger_config import Logging
import pandas as pd
import chess
import time
import os

load_dotenv()

log_config = Logging()
logger = log_config.get_logger('valuenetwork')


class ValueNetwork:
    
    def __init__(self):
        self.network = None
        self.model_path = 'backend/engine/agents/pythonAgents/evaluations/models/value_network.h5'
        self.dataset_path = os.getenv('DATASET_PATH')
        self.ChessData = None
        self.load_network()
        
    def load_network(self):
        if not self._file_path_exists(self.model_path):
            self.train_network()
        else:
            self.network = self.load_model(self.model_path)
        ...
        
    def load_model(self, model_path):
        logger.info(f'Loading model from {model_path}')
        return None
        
    def train_network(self):
        self.load_data()
        
        self.view_dataset()
        
    def evaluate_position(self, board: chess.Board) -> float:
        ...
        
    def load_data(self, sample_size=1000):
        logger.info('Loading initial dataset ChessData')
        data = pd.read_csv(self.dataset_path)
        
        self.ChessData = data.sample(n=sample_size)
        
        for idx, row in self.ChessData.iterrows():
            print('here')
            print('here')
            print(row)
            print('here')
            break
        
    def view_dataset(self):
        logger.info(' Summary of ChessData: ')
        logger.info(self.ChessData.head())
        
    @staticmethod
    def _file_path_exists(file_path):
        return Path(file_path).is_file()
