from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from engine.chess_engine import ChessEngine

class WebSocketService:
    def __init__(self, chess_engine: ChessEngine):
        self.app = Flask(__name__)
        CORS(self.app)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        self.chess_engine = chess_engine
        self._register_handlers()

    def _register_handlers(self):   
        @self.socketio.on('new_game')
        def handle_new_game(data):
            print('new_game', data)
            self.socketio.start_background_task(self.chess_engine.setup_game_environment, 
                                                **data, socket=self.socketio, 
                                                connect_web_sockets=True)

        @self.socketio.on('new_move')
        def handle_new_move(data):
            print('new_move', data)
            
    def start_server(self):
        self.socketio.run(self.app, host='0.0.0.0', port=5000, debug=False)