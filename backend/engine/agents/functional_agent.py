from engine.agents.evaluations.simple_eval import SimpleEvaluation
from engine.agents.searchTree.simpleTreeSearch import SimpleTreeSearch
from engine.utils.agent_utils import get_legal_moves_for_turn


class FunctionalAgent:
    
    def __init__(self):
        self.id = '0004'
        self.name = 'FunctionalEngine'
        self.search_params = {
            'evaluation': SimpleEvaluation(),
            'max_depth': 4,
            'verbose': True
        }
        self.search = SimpleTreeSearch(**self.search_params)
        
    def make_move(self, board, verbose=False):
                
        optimal_move, optimal_value = self.search.search(board)
        
        if verbose:
            print(f'Optimal move: {optimal_move} ({optimal_value})')
        
        return optimal_move