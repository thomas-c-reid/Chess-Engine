import chess

# TODO: 
# 1. Taking a pawn which would cause doubled pawns is good
# 2. Taking a pawn which would cause isolated pawns is good
# 3. is a piece pinned?

class SimpleEvaluation:
    def __init__(self):
        self.piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0,
        }
    
    def evaluate_position(self, board):
        """
        params:
        - board: (chess.Board) the current board state
        
        output:
        - (int) a score for the current board state (positive for white, negative for black)
        """
        score = 0
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                value = self.piece_values[piece.piece_type]
                if piece.color == chess.WHITE:
                    score += value
                else:
                    score -= value
        
        return score
    
