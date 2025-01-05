from random import choice
from engine.utils.agent_utils import get_legal_moves_for_turn


class RandomAgent:
    
    def __init__(self):
        self.id = '0001'
        self.name = 'RandomAgent'
        
    def make_move(self, board):
        legal_moves = list(get_legal_moves_for_turn(board))
        
        return choice(legal_moves)
