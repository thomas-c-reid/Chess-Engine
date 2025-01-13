from engine.agents.evaluations.piece_eval import PieceEvaluation
from engine.agents.searchTree.simpleTreeSearch import SimpleTreeSearch
from engine.utils.agent_utils import get_legal_moves_for_turn


class SimpleAgent:
    
    def __init__(self):
        self.id = '0003'
        self.name = 'SimpleAgent'
        self.search_params = {
            'evaluation': PieceEvaluation(),
            'max_depth': 2
        }
        self.search = SimpleTreeSearch(**self.search_params)
        
    def make_move(self, board):
        legal_moves = list(get_legal_moves_for_turn(board))
                
        
        optimal_move, optimal_value = self.search.search(board)
        
        return optimal_move