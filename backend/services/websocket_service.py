from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from chessArena.chess_engine import ChessEngine
from concurrent.futures import ThreadPoolExecutor
import asyncio
from utils.queue_utils import peek_asyncio_queue
import time

class WebSocketService:
    def __init__(self, move_queue, game_request_queue, game_acknowledgement_queue):
        self.app = Flask(__name__)
        CORS(self.app)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        self.executor = ThreadPoolExecutor(2)
        self.move_queue = move_queue
        self.game_request_queue = game_request_queue
        self.game_acknowledgement_queue = game_acknowledgement_queue
        self._register_handlers()

    # ROUTES - SHOULD BE MOVED TO NEW FILE
    def _register_handlers(self):
        @self.socketio.on('new_game')
        def handle_new_game(data):
            self.game_request_queue.put(data)
            
            game_processed = False
            while not game_processed:
                try:
                    game_processed = self.game_acknowledgement_queue.get(timeout=1)
                except asyncio.QueueEmpty:
                    pass
                time.sleep(0.1)  # Avoid busy waiting
            
            queue_info = peek_asyncio_queue(self.game_request_queue)
            
            print('data added to queue', queue_info)
            
        @self.socketio.on('new_move')
        def handle_new_move(data):            
            self.move_queue.put(data)

        @self.socketio.on('reset_game')
        def handle_game_reset(data):
            data = {'type': 'reset_game'}
            self.game_request_queue.put(data)
            
        @self.socketio.on('terminate_game')
        def handle_game_terminate():
            data = {'type': 'terminate_game'}
            self.game_request_queue.put(data)


    def start_server(self):
        print('listening on port 5000')
        self.socketio.run(self.app, host='0.0.0.0', port=5000, debug=False)

