import chess
import chess.polyglot
from tqdm import tqdm
import os
import random

class OpeningBook:
    
    def __init__(self, bin_url=None):
        self.book = {}
        if not bin_url:
            self.bin_url = os.path.join('engine', 'agents', 'pythonAgents', 'polyglotOpeningBooks', 'Titans.bin')
        else:
            self.bin_url = bin_url            
        self.load_opening_book(verbose=True)
        
    def decode_polyglot_move(self, hex_string):
        # Convert the hex string to bytes
        move_bytes = bytes.fromhex(hex_string)

        # Extract the "from-square" and "to-square" indices
        from_square = move_bytes[0]  # First byte
        to_square = move_bytes[1]    # Second byte

        # Convert these indices into algebraic notation using chess.SQUARE_NAMES
        from_square_algebraic = chess.SQUARE_NAMES[from_square]
        to_square_algebraic = chess.SQUARE_NAMES[to_square]

        # Combine them to form the move in standard notation
        move = from_square_algebraic + to_square_algebraic

        return move

    def load_opening_book(self, verbose=False):
        file_size = os.path.getsize(self.bin_url)
        with open(self.bin_url, 'rb') as opening_book, tqdm(total=file_size, unit='B', desc="Loading Opening Book", unit_scale=True) as pbar:
            while True:
                try:
                    key = opening_book.read(8)
                    if not key: 
                        break
                    pbar.update(8)
                    
                    move = opening_book.read(2).hex()
                    move_string = self.decode_polyglot_move(move)
                    
                    if not key: 
                        break
                    pbar.update(2)
                    
                    weight = int.from_bytes(opening_book.read(2), byteorder='big')
                    if not key: 
                        break
                    pbar.update(2)
                    _ = opening_book.read(4) # learn bytes?? or something
                    pbar.update(4)
                    
                    if key.hex() not in self.book:
                        self.book[key.hex()] = []
                        
                        self.book[key.hex()].append((move_string, weight))
                    else:
                        self.book[key.hex()].append((move_string, weight))
                    
                except Exception as e:
                    print(f'Error Reading File: {e}')
    
        if verbose:
            total_keys = len(self.book)
            total_moves = sum(len(moves) for moves in self.book.values())
            print(f"Total Keys (Positions): {total_keys}")
            print(f"Total Moves: {total_moves}")     
    
    def choose_opening_book_move(self, board):
        selected_move = None
                
        
        moves = []
        weights = []
        with chess.polyglot.open_reader(self.bin_url) as reader:
            for entry in reader.find_all(board):
                moves.append(entry.move)
                weights.append(entry.weight)
                
        if len(moves) > 0:
                
            total_weight = sum(weights)
            probabilities = [w / total_weight for w in weights]
                
            selected_move = random.choices(moves, probabilities, k=1)[0]
            
            print('Selected move from opening book', selected_move)
        
        return selected_move
    