from chessArena.chess_engine import ChessEngine
from services.websocket_service import WebSocketService
from services.move_analysis_service import MoveAnalysisService
from chessArena.game_handler import GameHandler
import multiprocessing as mp
import asyncio
import threading

class ThreadHandler():
    '''
    This class represents the handling of the muti threading websocket server.
    It will run an instance of the game on  a single process if no args passed
    '''    
    def __init__(self, move_analysis_queue: mp.Queue = None, game_handler_params: dict = None):
        self.move_analysis_queue = move_analysis_queue
        self.game_handler_params = game_handler_params
            
    async def setup_dual_threads(self):
        game_request_queue = asyncio.Queue()
        move_queue = asyncio.Queue()
        game_acknowledgement_queue = asyncio.Queue()      
        
        # SETUP SERVICES
        game_handler_params = {
            'game_request_queue': game_request_queue,
            'game_acknowledgement_queue': game_acknowledgement_queue,
            'move_queue': move_queue
        }
        game_handler = GameHandler(**game_handler_params)
        
        ws_params = {
            'move_queue': move_queue,
            'game_request_queue': game_request_queue,
            'game_acknowledgement_queue': game_acknowledgement_queue,
        }
        ws_service = WebSocketService(**ws_params)
        
        # SERVICE RUNNING FUNCTIONS
        def run_game_thread():
            print('Starting game thread')
            asyncio.run(game_handler.start_with_websockets())
            
        # CREATE THREADS
        game_thread = threading.Thread(target=run_game_thread)
        # ws_thread = threading.Thread(target=ws_service.start_server)
        
        # START THREADS
        game_thread.start()
        ws_thread.start()     
        
    def run_game_no_threads(self):
        game_handler = GameHandler()
        game_handler.start_without_websockets(self.game_handler_params)
    