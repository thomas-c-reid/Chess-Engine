from random import choice

class RandomAgent:
    
    def __init__(self):
        self.id = '0001'
        self.name = 'RandomAgent'
        
    def make_move(self, legal_moves):
        return choice(legal_moves)
