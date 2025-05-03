from chessArena.agents.pythonAgents.searchTree.simpleTreeSearch import SimpleTreeSearch
from chessArena.agents.base_agent import BaseAgent
from chessArena.utils.agent_utils import get_legal_moves_for_turn

class FunctionalAgent(BaseAgent):
    
    def __init__(self):
        super().__init__(id='0004', name='FunctionalEngine')
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
    
    
    chessArena