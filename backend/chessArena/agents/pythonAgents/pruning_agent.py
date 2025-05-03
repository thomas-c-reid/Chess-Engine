from chessArena.agents.pythonAgents.evaluations.simple_eval import SimpleEvaluation
from chessArena.agents.pythonAgents.searchTree.alphaBetaTreeSearch import minimax
from chessArena.agents.base_agent import BaseAgent
from chessArena.utils.agent_utils import get_legal_moves_for_turn
import time
import chess

class PruningAgent(BaseAgent):
    
    def __init__(self):
        super().__init__(id='0005', name='PruningAgent')
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