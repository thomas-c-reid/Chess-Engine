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
    fen_before_push: str
    taken_pieces: list
    
    def to_socket(self):
        
        promotion_piece = self.promotion if self._is_pawn_promotion(
            index_to_algebraic(self.from_square), index_to_algebraic(self.to_square)) else None
        
        # Build move dictionary
        move_dict = {'from': index_to_algebraic(self.from_square),
                     'to': index_to_algebraic(self.to_square)
                     }
        if promotion_piece:
            move_dict['promotion'] = promotion_piece
                        
        return {
            'gameId': str(self.game_id), 'player': self.player,
            'moveIdx': self.move_idx, 'time': str(self.time),
            'player': self.player,
            'move': move_dict,
            'fen_before_push': self.fen_before_push,
            'taken_pieces': self.taken_pieces
            };
        
    @staticmethod
    def _is_pawn_promotion(from_square: str, to_square: str) -> bool:
        """
        Determines if this move is a valid pawn promotion.
        - White pawns promote if they reach rank 8
        - Black pawns promote if they reach rank 1
        """
        # Extract rank (last character of the square)
        from_rank = int(from_square[1])
        to_rank = int(to_square[1])

        # White promotion (rank 7 → 8) or Black promotion (rank 2 → 1)
        return (from_rank == 7 and to_rank == 8) or (from_rank == 2 and to_rank == 1)
    
    def __str__(self):
        return f"GameId: {self.game_id}, player: {self.player}, move: {self.move}"
        pass