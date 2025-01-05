from engine.agents.evaluations.simple_eval import SimpleEvaluation
from engine.agents.searchTree.simpleTreeSearch import SimpleTreeSearch
from engine.utils.agent_utils import get_legal_moves_for_turn


class SimpleAgent:
    
    def __init__(self):
        self.id = '0003'
        self.name = 'SimpleAgent'
        self.search_params = {
            'evaluation': SimpleEvaluation(),
            'max_depth': 3
        }
        self.search = SimpleTreeSearch(**self.search_params)
        self.evaluation = SimpleEvaluation()
        
    def make_move(self, board):
        legal_moves = list(get_legal_moves_for_turn(board))
        
        # Could initially take a look at the board and with current time in mind, allocate an amount of thinking time to the problem
        
        
        optimal_move, optimal_value = self.search.search(board)
        
        return optimal_move
        
        # scores = []
        # for move in legal_moves:
        #     temp = deepcopy(board)
        #     temp.push(move)
        #     scores.append(self.evaluation.evaluate_position(temp))
            
        # if board.turn == 1:
        #     return legal_moves[scores.index(max(scores))]   
        # else:    
        #     return legal_moves[scores.index(min(scores))]   