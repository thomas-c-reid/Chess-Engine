import chess

def get_legal_moves_for_turn(board):
    # Check whose turn it is
    is_white_turn = board.turn

    # Get all legal moves
    legal_moves = list(board.legal_moves)  # Generates legal moves for both sides

    # Filter moves for the current player's turn
    if is_white_turn:
        # White's turn
        return [move for move in legal_moves if board.piece_at(move.from_square).color == chess.WHITE]
    else:
        # Black's turn
        return [move for move in legal_moves if board.piece_at(move.from_square).color == chess.BLACK]
