import argparse
from services.websocket_service import WebSocketService
from services.message_handler import MessageHandler
from engine.chess_engine import ChessEngine

def main():
    parser = argparse.ArgumentParser(description="Chess Engine for RL agents")
    parser.add_argument('-web', action='store_true', help="Enable web app")

    args = parser.parse_args()
    
    # message_handler = MessageHandler()
    chess_engine = ChessEngine()

    if args.web:
        ws_service = WebSocketService(chess_engine=chess_engine)
        ws_service.start_server()
        
    else:
        ...
        # websocket_service.start_game()
        
        # default_params = {
        #     'selected_player_names': ['OpeningBookAgent', 'RandomAgent'],
        #     'starts': 'P1',
        #     'game_length': '5min',
        #     'connect_web_sockets': False,
        #     'socket': None,
        #     'verbose': True
        # }
        
        # gamee_runner
        
if __name__ == '__main__':
    main()