from dataclasses import dataclass
from datetime import datetime
import json
from engine.utils.chess_logic_utils import index_to_algebraic

@dataclass
class MoveDto:
    game_id: str
    player: str
    move_idx: int
    from_square: str
    to_square: str
    drop: str
    promotion: str
    move: str
    time: str
    
    def to_socket(self):
        return {
            'gameId': str(self.game_id), 'player': self.player,
            'moveIdx': self.move_idx, 'time': str(self.time),
            'player': self.player,
            'move': {
                'from': index_to_algebraic(self.from_square),
                'to': index_to_algebraic(self.to_square),
                'promotion': 'q',
            }
            };
    
    def __str__(self):
        return f"GameId: {self.game_id}, player: {self.player}, move: {self.move}"
        pass