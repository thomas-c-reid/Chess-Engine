from chessArena.chess_engine import ChessEngine
from chessArena.enums.GameState import GameState
from chessArena.dtos.GameStateDto import GameStateDto
from chessArena.enums.GameState import GameState
from logger.logger_config import Logging
from utils.queue_utils import peek_asyncio_queue

logging_config = Logging()
logger = Logging.get_logger('GameHandler')

class GameHandler():
    '''
    
    '''
    def __init__(self, game_request_queue=None, move_queue=None, game_acknowledgement_queue=None):
        self.chess_engine = ChessEngine()
        self.game_request_queue = game_request_queue
        self.move_queue = move_queue
        self.game_acknowledgement_queue = game_acknowledgement_queue
        logger.info('Game handler instanciated')
        
    def start_without_websockets(self, params):
        logger.info('Starting game with Websocket connection')
        GameStateDto = self.chess_engine.setup_game_environment(**params)

        # Run game loop
        while GameStateDto.game_state != GameState.GAME_OVER:
                GameStateDto = self.chess_engine.make_move()

    async def start_with_websockets(self):
        logger.info('STARTING GAME WITH WEBSOCKET CONNECTION')
        while True:
            # wait for message off queue and handle i
            queue_contents = peek_asyncio_queue(self.game_request_queue)
            logger.info('Waiting on game_request queue ...', queue_contents)
            message = await self.game_request_queue.get()
            game_information = self.handle_game_request(message)
            if game_information:
                self.game_acknowledgement_queue.put(game_information.to_websocket())
            else:
                return False
            
            if game_information.game_state == 'WAITING':
                move = await self.move_queue.get()
                game_information = self.chess_engine.make_move(move)
                self.move_queue.put(game_information.to_websocket())
                
            if game_information.game_state == 'RUNNING':
                game_information = self.chess_engine.make_move()
                self.move_queue.put(game_information.to_websocket())
            
            if game_information.game_state == 'GAME_OVER':
                self.move_queue.put(game_information.to_websocket())
                
    def handle_game_request(self, message):
        if message['type'] == 'new_game':
            self.game_params = message['data']
            game_information = self.chess_engine.setup_game_environment(**message['data'])
            return game_information
        elif message['type'] == 'reset_game':
            game_information = self.chess_engine.setup_game_environment(**self.game_params)
            return game_information
        elif message['type'] == 'terminate_game':
            return False          
        