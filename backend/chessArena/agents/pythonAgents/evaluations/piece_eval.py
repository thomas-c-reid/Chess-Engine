import chess

class PieceEvaluation:
    def __init__(self):
        self.piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 200,
        }

    def evaluate_position(self, board: chess.Board) -> float:
        """
        Evaluate the chess position based on pieces on board. Nothing else
        
        Parameters:
        - board (chess.Board): The current board state.

        Returns:
        - float: A score for the current board state (positive for White, negative for Black).
        """
        score = 0

        # Material Evaluation
        score += self.material_evaluation(board)

        return score

    def material_evaluation(self, board):
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