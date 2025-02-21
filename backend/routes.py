from flask import Blueprint, request, jsonify
from engine.enums.GameLengthEnum import GameLengthEnum
import threading

# Define a Blueprint for API routes
api_routes = Blueprint("api_routes", __name__)

@api_routes.route('/start-match', methods=['POST'])
def start_match():
    """
    Request to start a chess match.
    """
    
    request_body = request.get_json()
    
    print('+'*50)
    print('Request Body:')
    print(request_body)
    print('+'*50)
    
    # Access the shared instances
    socketio = api_routes.socketio
    chess_engine = api_routes.chess_engine

    if not socketio or not chess_engine:
        return jsonify({"error": "SocketIO or ChessEngine not initialized"}), 500
    
    request_body['connect_web_sockets'] = True
    request_body['socket'] = socketio
    # request_body['starting_fen'] = 'rnb2b1r/ppkpP2p/5ppn/q1pQ4/8/2P1P3/PP3PPP/RNB1KBNR w KQ - 1 8'
    print(request_body)

    def run_game():
        print("Game started in background thread...")
        print(request_body)
        chess_engine.setup_game_environment(**request_body)
        chess_engine.start_game(verbose=True)

    # Start the game in a background thread
    game_thread = threading.Thread(target=run_game)
    game_thread.start()

    return jsonify({"message": "Match Started Successfully"}), 200