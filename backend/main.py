import sys

sys.dont_write_bytecode = True

from engine.chess_engine import ChessEngine
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from routes import api_routes

# Create global instances
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize the ChessEngine with socketio
chess_engine = ChessEngine()
chess_engine.socketio = socketio  # Pass the socketio instance to ChessEngine

# Pass instances to the Blueprint
api_routes.chess_engine = chess_engine  # Set shared chess_engine
api_routes.socketio = socketio  # Set shared socketio

# Register routes
app.register_blueprint(api_routes, url_prefix="/api")

if __name__ == '__main__':
    socketio.run(app, debug=False, host="localhost", port=5000)
