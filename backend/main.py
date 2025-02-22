import sys

sys.dont_write_bytecode = True

from engine.chess_engine import ChessEngine
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from routes import api_routes
import argparse
import asyncio

parser = argparse.ArgumentParser(description="Chess Engine with Command-Line Arguments")
parser.add_argument('-web', action='store_true', help="Enable web app")

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

chess_engine = ChessEngine()
chess_engine.socketio = socketio  # Pass the socketio instance to ChessEngine

api_routes.chess_engine = chess_engine
api_routes.socketio = socketio

# Register routes
app.register_blueprint(api_routes, url_prefix="/api")

async def run_game():
    params = {
        'selected_player_names': ['OpeningBookAgent', 'ManualPlay'],
        'starts': 'P1',
        'game_length': '5min',
        'connect_web_sockets': True,
        'socket': chess_engine.socketio,
        'verbose': True
    }
    await chess_engine.setup_game_environment(**params)
    await chess_engine.start_game(verbose=True)

if __name__ == '__main__':
    args = parser.parse_args()

    if args.web:
        socketio.run(app, debug=False, host="localhost", port=5000)
    else:
        async def main():
            params = {
                'selected_player_names': ['OpeningBookAgent', 'RandomAgent'],
                'starts': 'P1',
                'game_length': '5min',
                'connect_web_sockets': False,
                'socket': None,
                'verbose': True
            }
            await chess_engine.setup_game_environment(**params)
            await chess_engine.start_game(verbose=True)

        asyncio.run(main())
        # chess_engine.start_game(verbose=True)
