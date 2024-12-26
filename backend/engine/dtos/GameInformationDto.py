class GameInformationDto:
    
    def __init__(self, white_player, black_player, game_length):
        self.white_player = white_player
        self.black_player = black_player
        self.game_length = game_length
        self.moves = []
        self.result = None
    
    def __str__(self):
        
        return f'##### Game Information #####  \
            [  ] Game length: {self.game_length} \
            \n [x] White: {self.white_player.name} \
                \n [o] Black: {self.black_player.name} \
                    \n Moves: {self.moves}'