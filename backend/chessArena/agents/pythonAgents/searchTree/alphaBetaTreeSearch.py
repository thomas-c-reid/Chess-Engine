import chess
from copy import deepcopy
from chessArena.agents.pythonAgents.evaluations.simple_eval import SimpleEvaluation
from chessArena.utils.agent_utils import get_legal_moves_for_turn
from datetime import datetime

class Node:
    def __init__(self, board, value, parent=None, id=None, move=None):
        self.id = id
        self.board = board
        self.value = value
        self.is_expanded = False
        self.parent = parent
        self.children = []
        self.move=move
        self.visit_count = 0
    
    def inc_vis_count(self):
        self.visit_count += 1
        
        
class SearchTree:
    def __init__(self, root_board):
        self.root_node = Node(id=0, board=root_board, value=0)
        self.id_counter = 1
        self.nodes = []
    
    def add_node(self, node):
        node.id = self.id_counter
        self.id_counter += 1
        self.nodes.append(node)
        
    def find_node(self, board):
        for node in self.nodes:
            if node.board == board:
                return node
        return None
    
    def find_dupes(self):
        board_dict = {}
        duplicates = []
        for index, node in enumerate(self.nodes):
            board_fen = node.board.fen()
            if board_fen in board_dict:
                duplicates.append((board_dict[board_fen], index))
            else:
                board_dict[board_fen] = index
        return duplicates
    
    def __str__(self):
        return f"SearchTree with {len(self.nodes)} nodes"
    

class AlphaBetaTreeSearch:
    """
    
    """
    def __init__(self, evaluation=SimpleEvaluation(), max_depth=3, verbose=True):
        self.evaluation = evaluation
        initial_board = chess.Board()
        self.search_tree = SearchTree(initial_board)
        print(self.search_tree)
        self.max_depth = max_depth
        self.nodes_expanded = 0
        self.verbose = verbose
                    
            
    def expand_node(self, node, depth, verbose=False):
        self.nodes_expanded += 1        

        # Ensure we only get legal moves for the current player's turn
        # legal_moves = list(node.board.legal_moves)
        legal_moves = list(get_legal_moves_for_turn(node.board))
        children = []
        
        for move in legal_moves:
            temp_board = deepcopy(node.board)
            temp_board.push(move)
            new_node = Node(board=temp_board, value=0, parent=node, move=move)
            self.search_tree.add_node(new_node)
            children.append(new_node)
            
        if verbose:
            print('*' * 50)
            print(f'Expanding node at depth {depth}:', self.nodes_expanded)
            print(node.board)
            print(f'Node expanded with {len(legal_moves)} children')
            print('*' * 50)
            
        node.children = children

    def search(self, board: chess.Board):
        
        start_time = datetime.now()
        
        self.search_tree = SearchTree(board)
        self.nodes_visited = 0
        node = Node(board, 0)
        optimal_move, optimal_value = self._search(node, 0, alpha=float('-inf'), beta=float('inf'))
        
        if self.verbose:
            print('#################### Starting search ####################')
            print(f"Search completed. Search tree size: {len(self.search_tree.nodes)} nodes")
            print(f"Nodes visited: {self.nodes_visited}")
            print(f'Time taken: {datetime.now() - start_time}')
            for child_node in node.children:
                print(f'move: {child_node.move} ({child_node.value}) - ({child_node.visit_count})')
            print('#################### Finished search ####################')
        return optimal_move, optimal_value

        
    def _search(self, node, depth, alpha, beta):
        node.inc_vis_count()
        self.nodes_visited += 1
        
        if depth == self.max_depth:
            node.value = self.evaluation.evaluate_position(node.board)
            return node.move, node.value  # No move to associate, only value

        if not node.is_expanded:
            self.expand_node(node, depth)
            node.is_expanded = True

        if not node.children:  # No legal moves, game over or stalemate
            node.value = self.evaluation.evaluate_position(node.board)
            return node.move, node.value

        best_move = None
        if node.board.turn == 1:  # Maximizing player
            max_value = float('-inf')
            for child in node.children:
                move, value = self._search(child, depth + 1, alpha, beta)
                if value > max_value:
                    max_value = value
                    best_move = child.board.move_stack[-1]  # The move that led to this board
                    # best_move = move
                node.value = max_value
                alpha = max(alpha, max_value)
                if alpha <= beta:
                    break
            if best_move and not node.board.is_legal(best_move):
                print(f"Illegal move detected: {best_move}")
                best_move = None
            return best_move, max_value
        
        else:  # Minimizing player
            min_value = float('inf')
            for child in node.children:
                move, value = self._search(child, depth + 1, alpha, beta)
                if value < min_value:
                    min_value = value
                    # best_move = move
                    best_move = child.board.move_stack[-1]  # The move that led to this board
                node.value = min_value
                    
                beta = min(beta, min_value)
                if beta <= alpha:
                    break
                    
            if best_move and not node.board.is_legal(best_move):
                print(f"Illegal move detected: {best_move}")
                best_move = None
            return best_move, min_value


###########################################################################        
class minimax:
    def __init__(self, max_depth, evaluation=SimpleEvaluation(), verbose=True):
        self.evaluation = evaluation
        self.max_depth = max_depth
        self.verbose = verbose
    
    @staticmethod
    def _make_move(board, move):
        _board: chess.Board = deepcopy(board)
        _board.push(move)
        return _board

    def search(self, board: chess.Board, verbose=True):
        
        start_time = datetime.now()
        self.nodes_visited = 0
        self.nodes_evaluated = 0
        metadata = {}
        best_move, best_value = self._search(board, self.max_depth, maximizing_player=True, metadata=metadata)
        
        if verbose:
            print('#'*20)
            print(f'Time taken: {datetime.now() - start_time}')
            print(f'nodes evaluated: {self.nodes_evaluated}')
            print(f'Best move: {best_move} ({best_value})')
            print(f'metadata: {metadata}')
            print('#'*20)
        
        return best_move
        
        
    def _search(self, board: chess.Board, depth: int, maximizing_player: bool, alpha=float('-inf'), beta=float('inf'), metadata=None):
        if depth == 0 or board.is_game_over():
            self.nodes_evaluated += 1
            return None, self.evaluation.evaluate_position(board)
        
        legal_moves = get_legal_moves_for_turn(board)
        if maximizing_player:
            best_val = float('-inf')
            for move in legal_moves:
                _board = self._make_move(board, move)
                
                _, tmp = self._search(_board, depth-1, False, alpha, beta)
                
                if tmp > best_val:
                    best_val = tmp
                    best_move = move
                    
                if best_val >= beta:
                    break
                
                alpha = max(alpha, best_val)
                
                if metadata is not None and depth == self.max_depth:
                    metadata[move] =  tmp
        else:
            best_val = float('inf')
            for move in legal_moves:
                _board = self._make_move(board, move)
                
                _, tmp = self._search(_board, depth-1, True, alpha, beta)
                
                if tmp < best_val:
                    best_val = tmp
                    best_move = move
                    
                if best_val <= alpha:
                    break
                
                beta = min(beta, best_val)
                
                if metadata is not None and depth == self.max_depth:
                    metadata[move] =  tmp
        
        return best_move, best_val