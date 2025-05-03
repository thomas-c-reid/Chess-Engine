from random import choice
from chessArena.utils.agent_utils import get_legal_moves_for_turn
from chessArena.agents.base_agent import BaseAgent

class RandomAgent(BaseAgent):
    
    def __init__(self):
        super().__init__(id='0001', name='RandomAgent')
        
    def make_move(self, board):
        legal_moves = list(get_legal_moves_for_turn(board))
        
        return choice(legal_moves)
