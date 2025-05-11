from chessArena.chess_engine import ChessEngine
from services.websocket_service import WebSocketService
from services.move_analysis_service import MoveAnalysisService
from chessArena.game_handler import GameHandler
import multiprocessing as mp
import asyncio
import threading
import asyncio

class ThreadHandler():
    '''
    This class represents the handling of the muti threading websocket server.
    It will run an instance of the game on  a single process if no args passed
    '''    
    def __init__(self):
        ...
            
    async def run_dual_threads(self):
        game_request_queue = asyncio.Queue()
        outgoing_move_queue = asyncio.Queue()
        incoming_move_queue = asyncio.Queue()
        results_queue = asyncio.Queue()
        
        # SETUP SERVICES
        game_handler_params = {
            'game_request_queue': game_request_queue,
            'outgoing_move_queue': outgoing_move_queue,
            'incoming_move_queue': incoming_move_queue,
            'results_queue': results_queue
        }
        game_handler = GameHandler(**game_handler_params)
        
        ws_params = {
            'game_request_queue': game_request_queue,
            'outgoing_move_queue': outgoing_move_queue,
            'incoming_move_queue': incoming_move_queue,
            'results_queue': results_queue
        }
        ws_service = WebSocketService(**ws_params)
        
        await asyncio.gather(
            game_handler.start_with_websockets(),
            ws_service.start_server()
        )
        
        print('huh')
        
        
        # # SERVICE RUNNING FUNCTIONS
        # def run_game_thread():
        #     print('Starting game thread')
        #     asyncio.run(game_handler.start_with_websockets())
            
        # # CREATE THREADS
        # game_thread = threading.Thread(target=run_game_thread)
        # ws_thread = threading.Thread(target=ws_service.start_server)
        
        # # START THREADS
        # game_thread.start()
        # ws_thread.start()     
        
    def run_game_no_threads(self, game_handler_params):
        game_handler = GameHandler()
        game_handler.start_without_websockets(game_handler_params)
    