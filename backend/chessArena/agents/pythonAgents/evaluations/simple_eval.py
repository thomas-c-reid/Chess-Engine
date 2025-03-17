# # TODO: 
# # 1. Taking a pawn which would cause doubled pawns is good
# # 2. Taking a pawn which would cause isolated pawns is good
# # 3. is a piece pinned?

import chess

class SimpleEvaluation:
    def __init__(self):
        self.piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 200,
        }

        self.piece_square_tables = {
            chess.KING: [
                0, 0,  0,  0,   0,  0,  0, 0, 
                0, 0,  0,  0,   0,  0,  0, 0,
                0, 0,  0,  0,   0,  0,  0, 0,
                0, 0,  0,  0,   0,  0,  0, 0,
                0, 0,  0,  0,   0,  0,  0, 0,
                0, 0,  0,  0,   0,  0,  0, 0,
                0, 0,  0, -5,  -5, -5,  0, 0,
                0, 0, 10, -5,  -5, -5, 10, 0
                ],
            chess.QUEEN: [
                -20, -10, -10, -5, -5, -10, -10, -20,
                -10,   0,   0,  0,  0,   0,   0, -10,
                -10,   0,   5,  5,  5,   5,   0, -10,
                -5,   0,   5,  5,  5,   5,   0,  -5,
                -5,   0,   5,  5,  5,   5,   0,  -5,
                -10,   5,   5,  5,  5,   5,   0, -10,
                -10,   0,   5,  0,  0,   0,   0, -10,
                -20, -10, -10,  0,  0, -10, -10, -20],
            chess.ROOK: [
                10,  10,  10,  10,  10,  10,  10,  10,
                10,  10,  10,  10,  10,  10,  10,  10,
                0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,  10,  10,   0,   0,   0,
                0,   0,   0,  10,  10,   5,   0,   0],
            chess.BISHOP: [
                0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0,   0,   0,   0,   0,   0,
                0,  10,   0,   0,   0,   0,  10,   0,
                5,   0,  10,   0,   0,  10,   0,   5,
                0,  10,   0,  10,  10,   0,  10,   0,
                0,  10,   0,  10,  10,   0,  10,   0,
                0,   0, -10,   0,   0, -10,   0,   0],
            chess.KNIGHT: [ value * 0.1 for value in 
               [-5,  -5, -5, -5, -5, -5,  -5, -5,
                -5,   0,  0, 10, 10,  0,   0, -5,
                -5,   5, 10, 10, 10, 10,   5, -5,
                -5,   5, 10, 15, 15, 10,   5, -5,
                -5,   5, 10, 15, 15, 10,   5, -5,
                -5,   5, 10, 10, 10, 10,   5, -5,
                -5,   0,  0,  5,  5,  0,   0, -5,
                -5, -10, -5, -5, -5, -5, -10, -5]],
            chess.PAWN: [
                0,   0,   0,   0,   0,   0,   0,   0,
                30,  30,  30,  40,  40,  30,  30,  30,
                20,  20,  20,  30,  30,  30,  20,  20,
                10,  10,  15,  25,  25,  15,  10,  10,
                5,   5,   5,  20,  20,   5,   5,   5,
                5,   0,   0,   5,   5,   0,   0,   5,
                5,   5,   5, -10, -10,   5,   5,   5,
                0,   0,   0,   0,   0,   0,   0,   0]
        }

    def evaluate_position(self, board: chess.Board) -> float:
        """
        Evaluate the chess position.
        
        Parameters:
        - board (chess.Board): The current board state.

        Returns:
        - float: A score for the current board state (positive for White, negative for Black).
        """
        score = 0
        

        # Material Evaluation
        material_score = self.material_evaluation(board)

        # score += self.evaluate_pawn_structure(board)

        # Scores high if lotsW of moves present in future - I dont really like this
        # score += 0.1 * (len(list(board.legal_moves)) * (1 if board.turn == chess.WHITE else -1))

        piece_square_score = self.evaluate_piece_square_tables(board)
        piece_square_score = 0
        score = piece_square_score + material_score
        # print(f'score {score} piece_score {piece_square_score} mat_score {material_score}')
        
        return score

    def evaluate_pawn_structure(self, board: chess.Board) -> float:
        """
        Evaluate pawn structure (doubled, blocked, isolated pawns).

        Parameters:
        - board (chess.Board): The current board state.

        Returns:
        - float: The pawn structure evaluation score.
        """
        score = 0

        for color in [chess.WHITE, chess.BLACK]:
            pawns = board.pieces(chess.PAWN, color)
            pawns_by_file = [0] * 8

            for square in pawns:
                file = chess.square_file(square)
                pawns_by_file[file] += 1

                # Blocked pawn: A pawn that cannot advance because of another piece
                if color == chess.WHITE and board.piece_at(square + 8):
                    score -= 0.5 if color == chess.WHITE else -0.5
                elif color == chess.BLACK and board.piece_at(square - 8):
                    score -= 0.5 if color == chess.WHITE else -0.5

            # Doubled pawns: Two pawns on the same file
            for count in pawns_by_file:
                if count > 1:
                    score -= 0.5 * (count - 1) if color == chess.WHITE else -0.5 * (count - 1)

            # Isolated pawns: Pawns with no friendly pawns on adjacent files
            for file in range(8):
                if pawns_by_file[file] > 0:
                    is_isolated = True
                    if file > 0 and pawns_by_file[file - 1] > 0:
                        is_isolated = False
                    if file < 7 and pawns_by_file[file + 1] > 0:
                        is_isolated = False

                    if is_isolated:
                        score -= 0.5 if color == chess.WHITE else -0.5

        return score

    def evaluate_piece_square_tables(self, board: chess.Board) -> float:
        """
        Evaluate position based on piece-square tables.

        Parameters:
        - board (chess.Board): The current board state.

        Returns:
        - float: The positional score.
        """
        score = 0

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.piece_type in self.piece_square_tables:
                table = self.piece_square_tables[piece.piece_type]
                position_value = table[square if piece.color == chess.WHITE else chess.square_mirror(square)]
                score += position_value if piece.color == chess.WHITE else -position_value

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