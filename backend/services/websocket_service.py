from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from engine.chess_engine import ChessEngine
import asyncio
from concurrent.futures import ThreadPoolExecutor

class WebSocketService:
    def __init__(self, chess_engine: ChessEngine):
        self.app = Flask(__name__)
        CORS(self.app)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        self.chess_engine = chess_engine
        self.executor = ThreadPoolExecutor(2)  # Executor for running async tasks in background
        self._register_handlers()

    def _register_handlers(self):   
        @self.socketio.on('new_game')
        def handle_new_game(data):
            print('new_game', data)
            self.socketio.start_background_task(self.run_game_setup, **data)

        @self.socketio.on('new_move')
        def handle_new_move(data):
            print('new_move', data)
            self.chess_engine.receive_manual_move(move=data)

    def run_game_setup(self, **data):
        self.socketio.start_background_task(self.setup_and_start_game, **data)

    def setup_and_start_game(self, **data):
        """Now it's synchronous, so no need for an event loop."""
        self.chess_engine.setup_game_environment(**data, socket=self.socketio, connect_web_sockets=True)
        self.chess_engine.start_game(verbose=True)

    def start_server(self):
        self.socketio.run(self.app, host='0.0.0.0', port=5000, debug=False)

