class GameInformationDto:
    
    def __init__(self, white_player, black_player, game_length, board, game_state, game_id, last_move=None):
        self.white_player = white_player
        self.black_player = black_player
        self.game_length = game_length
        self.result = None
        self.board = board
        self.game_state = game_state
        self.last_move = last_move
        self.game_id = game_id
    
    def __str__(self):
        
        return f'##### Game Information #####  \
           \n [INFO] Game length: {self.game_length} \
            \n [x] White: {self.white_player["name"]} \
                \n [o] Black: {self.black_player["name"]} \
                    \n#############################'
    
    def to_websocket(self):
        return {
            'white': self.white_player['name'],
            'black': self.black_player['name'],
            'game_length': self.game_length,
            'starting_fen': self.board.fen()
        }
