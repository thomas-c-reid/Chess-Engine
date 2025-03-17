from abc import ABC, abstractmethod

class BaseAgent(ABC):
    
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        
    def __str__(self):
        return f"{self.name}"
    
    @abstractmethod
    def make_move(self, board):
        pass