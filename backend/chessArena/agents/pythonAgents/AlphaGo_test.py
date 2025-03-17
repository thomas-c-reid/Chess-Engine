from chessArena.agents.pythonAgents.evaluations.simple_eval import SimpleEvaluation
from chessArena.agents.base_agent import BaseAgent
from chessArena.agents.pythonAgents.evaluations.ValueNetwork import ValueNetwork

class AlphaGoAgent(BaseAgent):
    
    def __init__(self):
        super().__init__(id='0007', name='AlphaGoAgent')
        # self.search_params = {
        #     'evaluation': SimpleEvaluation(), 
        #     'max_depth': 4,
        #     'verbose': True
        # }
        # self.search = MCTS(**self.search_params)
        
        # TODO: refactor MCTS algorithm so that it works more efficiently 
        # TODO: Implement Value network which analyzes the board state and outputs a value representing the likelihood of winning
        # TODO: implement Policy network which analyzes the board state and outputs a probability distribution over possible moves
        self.network = ValueNetwork()
        
    def make_move(self, board, verbose=False):
                
        optimal_move, optimal_value = self.search.search(board)
        
        if verbose:
            print(f'Optimal move: {optimal_move} ({optimal_value})')
        
        return optimal_move