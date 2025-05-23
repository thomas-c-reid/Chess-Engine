from chessArena.agents.pythonAgents.evaluations.piece_eval import PieceEvaluation
from chessArena.agents.pythonAgents.searchTree.simpleTreeSearch import SimpleTreeSearch
from chessArena.utils.agent_utils import get_legal_moves_for_turn
from chessArena.agents.decorators.DelayAgent import DelayAgent

class SimpleAgent:
    
    def __init__(self):
        self.id = '0003'
        self.name = 'SimpleAgent'
        self.search_params = {
            'evaluation': PieceEvaluation(),
            'max_depth': 2
        }
        self.search = SimpleTreeSearch(**self.search_params)
        
    @DelayAgent()
    def make_move(self, board):
        legal_moves = list(get_legal_moves_for_turn(board))
                
        
        optimal_move, optimal_value = self.search.search(board)
        
        return optimal_move