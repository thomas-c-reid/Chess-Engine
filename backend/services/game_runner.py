import asyncio
from threading import Thread
from engine.chess_engine import ChessEngine
from backend.services.message_handler import MoveHandler

class GameRunner:
    def __init__(self, chess_engine: ChessEngine, move_handler: MoveHandler):
        self.chess_engine = chess_engine
        self.move_handler = move_handler
        self._running = False
        self._thread = None

    def start_game(self, params):
        
        def run_async():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self._run_game(params))
            
        self._running = True
        self._thread = Thread(target = run_async)
        self._thread.start()
        
    async def _run_game(self, params):
        await self.chess_engine.setup_game_environment(**params)
        await self.chess_engine.start_game(verbose=True)

    def stop_game(self):
        self._running = False
        if self._thread:
            self._thread.join()