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
from services.message_handler import MessageHandler


log_config = Logging()
logger = log_config.get_logger()

class ChessEngine:
        
    def __init__(self, message_handler: MessageHandler = None):
        self.board = chess.Board()
        self.message_handler = message_handler
        
        backend_dir = os.path.dirname(os.path.realpath(__file__))  # Path to the current file's directory
        project_root = os.path.abspath(os.path.join(backend_dir, '../../'))
        yaml_file_path = os.path.join(project_root, 'chess-client/public/agent_info.yaml')
        
        with open(yaml_file_path, 'r') as file:
            agent_config = yaml.safe_load(file)
            self.agents = agent_config.get('agents')   
        self.connected = False
        self.loop = asyncio.get_event_loop()
        self.manual_move_event = asyncio.Event()
        self.manual_move = None
        self.websocket_logger = log_config.get_logger('websocket')
                         
    def setup_game_environment(self, selected_player_names: list = [], starts: str = 'RAND', game_length: str ='5min', 
                               connect_web_sockets: bool = False, socket=None, verbose=False, starting_fen=None):
        """
        params:
        - starts: (str) a choice from: RAND, P1, P2 - decides who starts as White
        - GameLength: (Enum) 
        """        
        self.manual_move = None
                           
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
            module = importlib.import_module('engine.agents.random_agent')
            agent_class = getattr(module, 'RandomAgent')
            self.players.append({'name': 'RandomAgent', 'input_type': 'AUTO', 'class': agent_class()})
                                
                                
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
                            
            
        if starting_fen:
            print("starting fen", starting_fen)
            self.board.set_fen(starting_fen)
            
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

    def wait_for_manual_move(self):
        """This is now synchronous and will block the current thread until a move is received."""
        print('Waiting for manual move...')
        self.socketio.emit('')
        
        self.manual_move_event.clear()  # Reset the event
        while not self.manual_move_event.is_set():  # This will block the thread until the event is set
            pass
        
        
        if not self.manual_move:
            raise RuntimeError('No Move received from manual player')
        
        move_data = self.manual_move['move']
        
        # Log the move received
        self.websocket_logger.info(f'Move received: {move_data}')
    
        # Convert 'a7' to square index (0-63)
        def parse_square(square_str):
            file = square_str[0].lower()
            rank = square_str[1]
            file_number = ord(file) - ord('a')  # a=0, b=1, ..., h=7
            rank_number = int(rank) - 1        # Converts "7" to 6 (0-based)
            return chess.square(file_number, rank_number)
        
        from_square = parse_square(move_data['from'])
        to_square = parse_square(move_data['to'])
        
        # Handle promotion conversion ('q' -> chess.QUEEN)
        promotion_str = move_data.get('promotion')
            
        # Get the piece that is moving
        moved_piece = self.board.piece_at(from_square)

        # Handle promotion conversion ('q' -> chess.QUEEN), but ONLY if it's a pawn move
        promotion = None
        if promotion_str and moved_piece and moved_piece.piece_type == chess.PAWN:
            promotion = {"q": chess.QUEEN, "r": chess.ROOK, "b": chess.BISHOP, "n": chess.KNIGHT}.get(promotion_str.lower())   
        
        # Create the move object
        move = chess.Move(from_square, to_square, promotion=promotion)

        self.manual_move = None  # Reset the manual move after processing
        
        return move
    
    def receive_manual_move(self, move):
        """This will be called from the WebSocketService when a move is received."""
        self.manual_move = move
        self.manual_move_event.set()  # Trigger the event
        print(f'Move received: {move}') 
           
    def start_game(self, verbose=False):                        
        gameId = uuid4()
            
        turn = 0
        move_idx = 1
        game_over = False
        captured_pieces = {'white': [], 'black': []}
        
        # Game loop
        while not game_over:
            if turn == 0:
                # White player takes turn                
                if self.white_player['input_type'] == 'AUTO':
                    move_action: chess.Move = self.white_player['class'].make_move(self.board)
                elif self.white_player['input_type'] == 'MANUAL':
                    self.socketio.emit('request_move', None)
                    move_action = self.wait_for_manual_move()
                
                self.update_captured_pieces(move_action, 'white')  
                
                move = MoveDto(game_id=gameId, move=move_action.uci(), 
                            player='White', move_idx=move_idx, 
                            time=datetime.now(), from_square=move_action.from_square,
                            to_square=move_action.to_square, promotion=move_action.promotion,
                            drop=move_action.drop, fen_before_push=self.board.fen(), 
                            taken_pieces=self.taken_pieces)
            else:
                # Black player takes turn
                if self.black_player['input_type'] == 'AUTO':
                    move_action: chess.Move = self.black_player['class'].make_move(self.board)
                elif self.black_player['input_type'] == 'MANUAL':
                    logger.info('Need to implement async websocket move')
                    self.socketio.emit('request_move', None)
                    move_action = self.wait_for_manual_move()
                    
                self.update_captured_pieces(move_action, 'black')
                    
                move = MoveDto(game_id=gameId, move=move_action.uci(), 
                               player='Black', move_idx=move_idx, 
                               time=datetime.now(), from_square=move_action.from_square,
                               to_square=move_action.to_square, promotion=move_action.promotion,
                               drop=move_action.drop, fen_before_push=self.board.fen(),
                               taken_pieces=self.taken_pieces)
            
            if self.connected:
                data = move.to_socket()
                if turn == 0:
                    if self.white_player['input_type'] != 'MANUAL':
                        self.socketio.emit("new_move", {"move": str(data)})
                        self.websocket_logger.info(f'Sending move: {data}')
                        
                else:
                    if self.black_player['input_type'] != 'MANUAL':
                        self.socketio.emit("new_move", {"move": str(data)})
                        self.websocket_logger.info(f'Sending move: {data}')
                        
                
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
