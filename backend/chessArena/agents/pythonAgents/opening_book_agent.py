from chessArena.agents.pythonAgents.evaluations.simple_eval import SimpleEvaluation
from chessArena.agents.pythonAgents.searchTree.alphaBetaTreeSearch import minimax
from chessArena.agents.pythonAgents.openingBooks.openingBook import OpeningBook
from chessArena.agents.base_agent import BaseAgent
from chessArena.utils.agent_utils import get_legal_moves_for_turn
from tqdm import tqdm
import chess.polyglot
import chess
import time
import os

class OpeningBookAgent(BaseAgent):
    
    def __init__(self):
        super().__init__(id='0006', name='OpeningBookAgent')
        self.search_params = {
            'evaluation': SimpleEvaluation(),
            'max_depth': 4,
            'verbose': True
        }
        self.search = minimax(**self.search_params)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.bin_url = os.path.normpath(os.path.join(base_dir, '..', 'polyglotOpeningBooks', 'Titans.bin'))
        self.opening_book = OpeningBook()
           
    def load_opening_book(self, verbose=False):
        file_size = os.path.getsize(self.bin_url)
        
        with open(self.bin_url, 'rb') as opening_book, tqdm(total=file_size, unit='B', desc="Loading Opening Book") as pbar:
            while True:
                try:
                    key = opening_book.read(8)
                    if not key: 
                        break
                    pbar.update(8)
                    
                    move = opening_book.read(2)
                    move = (bytes.fromhex(move))
                    if not key: 
                        break
                    pbar.update(2)
                    
                    weight = int.from_bytes(opening_book.read(2), byteorder='big')
                    if not key: 
                        break
                    pbar.update(2)
                    _ = opening_book.read(4) # learn bytes?? or something
                    pbar.update(4)
                    
                    if key.hex() not in self.opening_book:
                        self.opening_book[key.hex()] = []
                        self.opening_book[key.hex()].append((move.hex(), weight))
                    else:
                        self.opening_book[key.hex()].append((move.hex(), weight))
                    
                    # print(f"Key: {key.hex()}, Move: {move}, Weight: {weight}")
                except Exception as e:
                    print(f'Error Reading File: {e}')
    
        if verbose:
            total_keys = len(self.opening_book)
            total_moves = sum(len(moves) for moves in self.opening_book.values())
            print(f"Total Keys (Positions): {total_keys}")
            print(f"Total Moves: {total_moves}")
    
    def choose_opening_book_move(self, board):
        is_move_made = False
                
        print('*'*50)
        print(f"Searching opening book")
        
        hash = format(chess.polyglot.zobrist_hash(board), '016x')
        
        print(hash)
        print(self.opening_book[hash])
        print('*'*50)
        
        
        return is_move_made
        
    def make_move(self, board: chess.Board, verbose=False):
        
        move = self.opening_book.choose_opening_book_move(board)
                
        if not move:        
            start_time = time.time()
            move = self.search.search(board)
            time_spent = time.time() - start_time
        
        if verbose:
            print('<>'*59)
            print('inside Pruning agent')
            print(board)
            print(get_legal_moves_for_turn(board))
            print(f'Optimal move: {move}')
            print(f'Time spent searching {time_spent}')
            print('<>'*59)
        
        return move