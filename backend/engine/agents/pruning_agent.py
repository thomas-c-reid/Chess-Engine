from engine.agents.evaluations.simple_eval import SimpleEvaluation
from engine.agents.searchTree.alphaBetaTreeSearch import AlphaBetaTreeSearch 
import time

class PruningAgent:
    
    def __init__(self):
        self.id = '0005'
        self.name = 'PruningAgent'
        self.search_params = {
            'evaluation': SimpleEvaluation(),
            'max_depth': 6,
            'verbose': True
        }
        self.search = AlphaBetaTreeSearch(**self.search_params)
        
    def make_move(self, board, verbose=False):
                
        start_time = time.time()
        optimal_move, optimal_value = self.search.search(board)
        time_spent = time.time() - start_time
        
        if verbose:
            print(f'Optimal move: {optimal_move} ({optimal_value})')
            print(f'Time spent searching {time_spent}')
        
        return optimal_move