from chessArena.dtos.GameInformationDto import GameInformationDto
from chessArena.dtos.MoveDto import MoveDto
from chessArena.enums.GameState import GameState
from logger.logger_config import Logging
from datetime import datetime
from random import choice
from uuid import uuid4
import importlib
import asyncio
import chess
import yaml
import time
import os 


log_config = Logging()
logger = log_config.get_logger('chess_engine')

class ChessEngine:
        
    def __init__(self):
        backend_dir = os.path.dirname(os.path.realpath(__file__))  # Path to the current file's directory
        project_root = os.path.abspath(os.path.join(backend_dir, '../../'))
        yaml_file_path = os.path.join(project_root, 'chess-client/public/agent_info.yaml')
        
        with open(yaml_file_path, 'r') as file:
            agent_config = yaml.safe_load(file)
            self.agents = agent_config.get('agents')   
        self.connected = False
                         
    def setup_game_environment(self, selected_player_names: list = [], 
                               starts: str = 'RAND', game_length: str ='5min',
                               starting_fen=None):
        """
        Will create a new instance of a game, load in the relevant players and set up the board.
        Should return a GameInformationDto object with the game information.
        """              
        self.game_id = uuid4()
        # load agents
        self.board = chess.Board()
        self.taken_pieces = {'white': [{'queen': 0}, {'rook': 0}, {'bishop': 0}, {'knight': 0}, {'pawn': 0}], 
                             'black': [{'queen': 0}, {'rook': 0}, {'bishop': 0}, {'knight': 0}, {'pawn': 0}]}
        self.load_agents(selected_player_names)            
        
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
            
        # set starting fen of board - if necessary
        if starting_fen:
            print("starting fen", starting_fen)
            self.board.set_fen(starting_fen)
            
        self.GameInformation = GameInformationDto(self.white_player, self.black_player, 
                                                  game_length, self.board, 
                                                  self.get_game_state(), self.game_id)
        logger.info(self.GameInformation)

        return self.GameInformation
    
    def load_agents(self, selected_player_names: list = []):
        self.players = []
        for selected_agent in selected_player_names:
            for agent_name, agent_info in self.agents.items():
                if agent_name == selected_agent:
                    if agent_info['input_type'] != 'MANUAL':

                        module = importlib.import_module(agent_info['file_location'])
                        agent_class = getattr(module, agent_name)
                        player_dict = {'name': agent_name,'input_type': agent_info['input_type'], 'class': agent_class()}
                    else:
                        player_dict = {'name': agent_name,'input_type': agent_info['input_type']}
                    self.players.append(player_dict)
                    
        for i in range(2 - len(self.players)):
            module = importlib.import_module('engine.agents.random_agent')
            agent_class = getattr(module, 'RandomAgent')
            self.players.append({'name': 'RandomAgent', 'input_type': 'AUTO', 'class': agent_class()})
                                 
    def make_move(self, move=None):
        if not move:
            if self.board.turn:
                move_action: chess.Move = self.white_player['class'].make_move(self.board)
            else:
                move_action: chess.Move = self.black_player['class'].make_move(self.board)
                
            self.update_captured_pieces(move_action)
            
            move =  MoveDto(self.game_id, move=move_action.uci(),
                            player='White' if self.board.turn else 'Black',
                            move_idx=1, time=datetime.now(), from_square=move_action.from_square,
                            to_square=move_action.to_square, promotion=move_action.promotion,
                            drop=move_action.drop, fen_before_push=self.board.fen(),
                            taken_pieces=self.taken_pieces)
            
        if isinstance(move, MoveDto):
            move = chess.Move.from_uci(move.move)
        elif isinstance(move, str):
            move = chess.Move.from_uci(move)   
         
        self.board.push(move)     
        # Now you need to build back up the GameInformationDto object to return to the client
    
        self.GameInformation.board = self.board
        self.GameInformation.game_state = self.get_game_state()
        self.GameInformation.last_move = move
        
        print('+'*50)
        print(self.board)
        print(move)        
        print('+'*50)
        
        return self.GameInformation
    
    def update_captured_pieces(self, move):
        """
        Update the taken_pieces list when a capture occurs
        
        Args:
            board: chess.Board() - the board before the move is made
            move: chess.Move() - the move being made
            color: str - 'white' or 'black' indicating who made the move
        """
        # Get the piece at the destination square before the move
        
        print(move)
        
        captured_square = self.board.piece_at(move.to_square)
        
        if captured_square is not None:  # If there was a piece at the destination
            # Determine which piece was captured
            piece_type = str(captured_square).lower()
            opponent = 'white' if self.board.turn else 'black'
            
            # Map piece symbol to name
            piece_map = {
                'q': 'queen',
                'r': 'rook',
                'b': 'bishop',
                'n': 'knight',
                'p': 'pawn'
            }
            
            if piece_type in piece_map:
                # Find the dictionary for the piece type in the opponent's list
                for piece_dict in self.taken_pieces[opponent]:
                    if piece_map[piece_type] in piece_dict:
                        piece_dict[piece_map[piece_type]] += 1
                        break    
            print('piece taken', self.taken_pieces)
    
    def get_game_state(self):
        if self.board.is_checkmate():
            winner = "Black" if self.board.turn else "White"
            logger.info(f"Game over! Winner: {winner}")
            game_state = GameState.GAME_OVER
        elif self.board.is_stalemate():
            logger.info("Game over! It's a stalemate.")
            game_state = GameState.GAME_OVER
        elif self.board.is_insufficient_material():
            logger.info("Game over! Draw due to insufficient material.")
            game_state = GameState.GAME_OVER
        elif self.board.is_seventyfive_moves():
            logger.info("Game over! Draw due to seventy-five-move rule.")
            game_state = GameState.GAME_OVER
        elif self.board.is_fivefold_repetition():
            logger.info("Game over! Draw due to fivefold repetition.")
            game_state = GameState.GAME_OVER
        else:
            game_state = GameState.RUNNING
            
        return game_state
    
    @staticmethod
    def change_turn(turn):
        if turn == 0:
            new_turn = 1
        else: 
            new_turn = 0
        return new_turn
