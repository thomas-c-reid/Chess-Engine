from chessArena.chess_engine import ChessEngine
from chessArena.enums.GameState import GameState
from chessArena.dtos.GameStateDto import GameStateDto
from chessArena.enums.GameState import GameState
from logger.logger_config import Logging
import asyncio

import os
from dotenv import load_dotenv
import yaml

load_dotenv()

logging_config = Logging()
logger = Logging.get_logger('GameHandler')

class GameHandler():
    '''
    
    '''
    def __init__(self, game_request_queue=None, incoming_move_queue=None, outgoing_move_queue=None, results_queue=None):
        # create Engine
        self.chess_engine = ChessEngine()
        
        # Load Queues
        self.game_request_queue = game_request_queue
        self.outgoing_move_queue = outgoing_move_queue
        self.incoming_move_queue = incoming_move_queue
        self.results_queue = results_queue
        
        # Load agent information
        self.agent_info_path = os.getenv('AGENT_CONFIG_PATH')
        if not self.agent_info_path:
            raise ValueError("AGENT_CONFIG_PATH is not set in the environment.")
        with open(self.agent_info_path, 'r') as file:
            self.agent_information = yaml.safe_load(file)
        
        # store a dict containing each players name and their input type
        logger.info('Game handler instanciated')
        
    def start_without_websockets(self, params):
        logger.info('Starting game with Websocket connection')
        GameStateDto = self.chess_engine.setup_game_environment(**params)

        # Run game loop
        while GameStateDto.game_state != GameState.GAME_OVER:
                GameStateDto = self.chess_engine.make_move()

    async def start_with_websockets(self):
        logger.info('STARTING GAME WITH WEBSOCKET CONNECTION')
        
        game_started = False
        while True:
            # wait for message off queue and handle i
            if not game_started:
                message = await self.game_request_queue.get()
                game_information = self.handle_game_request(message)
                game_started = True
                
            # White players turn
            if self.chess_engine.board.turn:
                if self.chess_engine.white_player.get('input_type') == 'AUTO':
                    game_information = self.chess_engine.make_move()
                else:
                    print('waiting on white to move...')
                    move = await self.incoming_move_queue.get()
                    game_information = self.chess_engine.make_move(move)
                print('SENDING WHITE MOVE TO MOVE QUEUE - type', type(game_information.to_websocket()))
                await self.outgoing_move_queue.put(game_information.to_websocket())
            # Black players turn
            else:
                if self.chess_engine.black_player.get('input_type') == 'AUTO':
                    game_information = self.chess_engine.make_move()
                else:
                    print('waiting on black to move...')
                    move = await self.incoming_move_queue.get()
                    game_information = self.chess_engine.make_move(move)
                print('SENDING BLACK MOVE TO MOVE QUEUE')
                await self.outgoing_move_queue.put(game_information.to_websocket())
                
            await asyncio.sleep(0)
                    
            if game_information.game_state == GameState.GAME_OVER:
                return False
           
        # TODO - Handle logic for viewing and sending results
        ...
             
    def handle_game_request(self, message):
        if message['type'] == 'new_game':
            print('-'*25)
            print(message)
            print('-'*25)
            self.game_params = message['game_request']
            game_information = self.chess_engine.setup_game_environment(**message['game_request'])
            return game_information
        elif message['type'] == 'reset_game':
            game_information = self.chess_engine.setup_game_environment(**self.game_params)
            return game_information
        elif message['type'] == 'terminate_game':
            return False          
        