from chessArena.chess_engine import ChessEngine
from services.websocket_service import WebSocketService
from services.move_analysis_service import MoveAnalysisService
from thread_handler import ThreadHandler
import multiprocessing as mp
import asyncio

class ProcessHandler():
    '''
    This class represents the handling of the Game on one process, and the move_analysis on a seperate process.
    1) first process will handle a non-websocket game
    It will run an instance of the game on  a single process if no args passed
    '''
    
    def __init__(self, connect_web_sockets: bool = False):

        move_queue = mp.Queue()            
            
        self.game_process = mp.Process(target=self.run_game, args=(connect_web_sockets, move_queue,))
        self.move_analysis_process = mp.Process(target=self.run_move_analysis)
        
        self.start()
    
    # process 1
    @staticmethod
    def run_game(connect_to_websocket: bool = False, move_queue: mp.Queue = None):
        print('running game on process')
        
        default_params = {
            'selected_player_names': ['RandomAgent', 'RandomAgent'],
            'starts': 'P1',
            'game_length': '5min',
        }
        
        thread_handler = ThreadHandler(move_analysis_queue=move_queue, 
                                       game_handler_params=default_params)
        
        if connect_to_websocket: 
            asyncio.run(thread_handler.setup_dual_threads())
        else:
            thread_handler.run_game_no_threads()
        
        
    # process 2
    @staticmethod
    def run_move_analysis():
        print('running move analysis on process')
        move_analysis_service = MoveAnalysisService(connect_web_sockets=False)
        
    # process commands
    def start(self):
        self.game_process.start()
        self.move_analysis_process.start()
        
        
    