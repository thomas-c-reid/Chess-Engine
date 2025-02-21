from engine.enums.GameLengthEnum import GameLengthEnum 
from engine.dtos.GameInformationDto import GameInformationDto
from logger.logger_config import Logging
from engine.dtos.MoveDto import MoveDto
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
logger = log_config.get_logger()

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
                               connect_web_sockets: bool = False, socket=None, verbose=False, starting_fen=None):
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
                    if agent_info['input_type'] != 'MANUAL':

                        module = importlib.import_module(agent_info['file_location'])
                        agent_class = getattr(module, agent_name)
                        player_dict = {'name': agent_name,'input_type': agent_info['input_type'], 'class': agent_class()}
                    else:
                        player_dict = {'name': agent_name,'input_type': agent_info['input_type']}
                    self.players.append(player_dict)
                    
        for i in range(2 - len(self.players)):
            self.players.append({'name': 'RandomAgent', 'input_type': 'AUTO', 'class': 'engine.agents.random_agent'})
                                
                                
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
                            
            
        if starting_fen is not None:
            try:
                self.board.set_fen(starting_fen)
                print(f'Board position:\n{self.board}\n{starting_fen}')
            except ValueError:
                print("Invalid FEN string provided.")
            print(f'board position \n {self.board}')
            
        self.GameInformation = GameInformationDto(self.white_player, self.black_player, game_length, self.board)
        if verbose:
            logger.info(self.GameInformation)
            
        self.taken_pieces = {'white': [{'queen': 0}, {'rook': 0}, {'bishop': 0}, {'knight': 0}, {'pawn': 0}], 
                             'black': [{'queen': 0}, {'rook': 0}, {'bishop': 0}, {'knight': 0}, {'pawn': 0}]}
            
        if connect_web_sockets:
            self.socketio = socket
            self.connected = True
            self.socketio.sleep(1)  # Allow WebSocket time to stabilize
            data = self.GameInformation.to_websocket()
            self.socketio.emit("new_game", data)
            print('SENDING NEW GAME WEBSOCKET')

    async def wait_for_manual_move(self):
        """
        Wait for a move to be received via WebSocket.
        """
        move = None
        event = asyncio.Event()

        # Define a callback to handle the received move
        def on_move_received(data):
            nonlocal move
            move = data['move']  # Assuming the move is sent as a 'move' field in the WebSocket message
            event.set()  # Notify that a move has been received

        # Register the WebSocket event listener
        self.socketio.on('new_move', on_move_received)

        # Wait until the move is received
        await event.wait()

        # Remove the listener to avoid potential conflicts
        self.socketio.off('new_move', on_move_received)

        return move

           
    def start_game(self, verbose=False):
        # TODO:
        logger.info('STARTING GAME')
        
        time.sleep(5)
        # need to change this to recieve a message from front end saying  'ready to go' or something
                
        gameId = uuid4()
            
        turn = 0
        move_idx = 1
        game_over = False
        captured_pieces = {'white': [], 'black': []}
        
        while not game_over:
            if turn == 0:
                print('White turn')
                # White player takes turn                
                if self.white_player['input_type'] == 'AUTO':
                    move_action: chess.Move = self.white_player['class'].make_move(self.board)
                elif self.white_player['input_type'] == 'MANUAL':
                    # need a function to wait for a move to come in through websockets
                    logger.info('Need to implement async websocket move')
                    
                print(move_action)
                
                self.update_captured_pieces(move_action, 'white')  
                
                move = MoveDto(game_id=gameId, move=move_action.uci(), 
                            player='White', move_idx=move_idx, 
                            time=datetime.now(), from_square=move_action.from_square,
                            to_square=move_action.to_square, promotion=move_action.promotion,
                            drop=move_action.drop, fen_before_push=self.board.fen(), 
                            taken_pieces=self.taken_pieces)
            else:
                print('Black turn')
                # Black player takes turn
                if self.black_player['input_type'] == 'AUTO':
                    move_action: chess.Move = self.black_player['class'].make_move(self.board)
                elif self.black_player['input_type'] == 'MANUAL':
                    logger.info('Need to implement async websocket move')
                    
                self.update_captured_pieces(move_action, 'black')
                    
                move = MoveDto(game_id=gameId, move=move_action.uci(), 
                               player='Black', move_idx=move_idx, 
                               time=datetime.now(), from_square=move_action.from_square,
                               to_square=move_action.to_square, promotion=move_action.promotion,
                               drop=move_action.drop, fen_before_push=self.board.fen(),
                               taken_pieces=self.taken_pieces)
                
            
            if self.connected:
                data = move.to_socket()
                print('+'*50)
                print('sending move to socket', data)
                print('+'*50)
                self.socketio.emit("new_move", {"move": str(data)})
                self.socketio.sleep(3)
                
            if isinstance(move, MoveDto):
                move = chess.Move.from_uci(move.move)
            elif isinstance(move, str):
                move = chess.Move.from_uci(move)

            self.board.push(move)
            
            # Check terminal state
            if self.board.is_checkmate():
                winner = "Black" if self.board.turn else "White"
                logger.info("Game over! Winner: ", winner)
                game_over = True
            elif self.board.is_stalemate():
                logger.info("Game over! It's a stalemate.")
                game_over = True
            elif self.board.is_insufficient_material():
                logger.info("Game over! Draw due to insufficient material.")
                game_over = True
            elif self.board.is_seventyfive_moves():
                logger.info("Game over! Draw due to seventy-five-move rule.")
                game_over = True
            elif self.board.is_fivefold_repetition():
                logger.info("Game over! Draw due to fivefold repetition.")
                game_over = True
            else:
                # Game continues
                turn = self.change_turn(turn)
                move_idx += 1
            
            if verbose:
                print(f'[{turn}] move', move)
                # print(self.board.fen())
                print(self.board)
                logger.info('*'*50)
        
    def update_captured_pieces(self, move, colour):
        """
        Update the taken_pieces list when a capture occurs
        
        Args:
            board: chess.Board() - the board before the move is made
            move: chess.Move() - the move being made
            color: str - 'white' or 'black' indicating who made the move
        """
        # Get the piece at the destination square before the move
        captured_square = self.board.piece_at(move.to_square)
        
        if captured_square is not None:  # If there was a piece at the destination
            # Determine which piece was captured
            piece_type = str(captured_square).lower()
            opponent = 'black' if colour == 'white' else 'white'
            
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
    
    @staticmethod
    def change_turn(turn):
        if turn == 0:
            new_turn = 1
        else: 
            new_turn = 0
        return new_turn
