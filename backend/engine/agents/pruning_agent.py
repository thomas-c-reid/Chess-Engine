from engine.agents.evaluations.simple_eval import SimpleEvaluation
from engine.agents.searchTree.alphaBetaTreeSearch import AlphaBetaTreeSearch 
from engine.utils.agent_utils import get_legal_moves_for_turn
from engine.agents.searchTree.alphaBetaTreeSearch import minimax
import time
import chess

class PruningAgent:
    
    def __init__(self):
        self.id = '0005'
        self.name = 'PruningAgent'
        self.search_params = {
            'evaluation': SimpleEvaluation(),
            'max_depth': 3,
            'verbose': True
        }
        # self.search = AlphaBetaTreeSearch(**self.search_params)
        self.search = minimax(**self.search_params)
        
    def make_move(self, board: chess.Board, verbose=False):
                
        start_time = time.time()
        optimal_move = self.search.search(board)
        time_spent = time.time() - start_time
        
        if verbose:
            print('<>'*59)
            print('inside Pruning agent')
            print(board)
            print(get_legal_moves_for_turn(board))
            print(f'Optimal move: {optimal_move}')
            print(f'Time spent searching {time_spent}')
            print('<>'*59)
        
        return optimal_move