from enum import Enum

class GameState(Enum):
    NOT_RUNNING = 1
    RUNNING = 2
    WAITING = 3
    GAME_OVER = 4