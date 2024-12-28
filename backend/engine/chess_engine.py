from engine.enums.GameLengthEnum import GameLengthEnum 
from engine.dtos.GameInformationDto import GameInformationDto
from engine.utils.agent_utils import get_legal_moves_for_turn
from engine.dtos.MoveDto import MoveDto
from datetime import datetime
from random import choice
from uuid import uuid4
import importlib
import chess
import yaml
import time
import os 

class ChessEngine:
    
    def __init__(self):
        self.board = chess.Board()
        
        backend_dir = os.path.dirname(os.path.realpath(__file__))  # Path to the current file's directory
        # Move up two directories to the project root
        project_root = os.path.abspath(os.path.join(backend_dir, '../../'))
        yaml_file_path = os.path.join(project_root, 'frontend/public/agent_info.yaml')
        
        with open(yaml_file_path, 'r') as file:
            agent_config = yaml.safe_load(file)
            self.agents = agent_config.get('agents')   
        self.connected = False
                         
    def setup_game_environment(self, selected_player_names: list = [], starts: str = 'RAND', game_length: str ='5min', 
                               connect_web_sockets: bool = False, socket=None):
        """
        params:
        - starts: (str) a choice from: RAND, P1, P2 - decides who starts as White
        - GameLength: (Enum) 
        """        
        # select players
        self.players = []
        for selected_agent in selected_player_names:
            for agent_name, agent_info in self.agents.items():
                if agent_name == selected_agent:                    
                    module = importlib.import_module(agent_info['file_location'])
                    agent_class = getattr(module, agent_name)
                    self.players.append(agent_class())
        
        # Select colour
        if starts == 'P1':
            self.white_player = self.players[0]
            self.black_player = self.players[1]
        elif starts == 'P2':
            self.black_player = self.players[0]
            self.white_player = self.players[1]
        else:
            self.white_player = choice(self.players)
            self.black_player = self.players[1 - self.players.index(self.white_player)]
            
        print(self.players)
            
        self.GameInformation = GameInformationDto(self.white_player, self.black_player, game_length)
        
        if connect_web_sockets:
            self.socketio = socket
            self.connected = True
           
    def start_game(self):
        # TODO: This function needs expanded - needs to be able to handle different users selected 
        
        time.sleep(5)
                
        gameId = uuid4()
            
        turn = 0
        move_idx = 1
        
        while not self.board.is_game_over():
            if turn == 0:
                # White player takes turn
                legal_moves = list(get_legal_moves_for_turn(self.board))
                move_action: chess.Move = self.white_player.make_move(legal_moves)
                move = MoveDto(game_id=gameId, move=move_action.uci(), 
                               player='White', move_idx=move_idx, 
                               time=datetime.now(), from_square=move_action.from_square,
                               to_square=move_action.to_square, promotion=move_action.promotion,
                               drop=move_action.drop)
            else:
                # Black player takes turn
                legal_moves = list(get_legal_moves_for_turn(self.board))
                move_action: chess.Move = self.black_player.make_move(legal_moves)
                move = MoveDto(game_id=gameId, move=move_action.uci(), 
                               player='Black', move_idx=move_idx, 
                               time=datetime.now(), from_square=move_action.from_square,
                               to_square=move_action.to_square, promotion=move_action.promotion,
                               drop=move_action.drop)
                
            print('*'*50)
            print('Move taken: ', move)
            print('turn: ', turn)
            print('*'*50)
            
            if self.connected:
                data = move.to_socket()
                print('Data', data)
                self.socketio.emit("new_move", {"move": str(data)})
                self.socketio.sleep(3)
                
            self.board.push(move)
            
            turn = self.change_turn(turn)  
            move_idx += 1
    
    @staticmethod
    def change_turn(turn):
        if turn == 0:
            new_turn = 1
        else: 
            new_turn = 0
        return new_turn
