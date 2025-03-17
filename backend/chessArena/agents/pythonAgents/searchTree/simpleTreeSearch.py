import chess
from copy import deepcopy
from engine.agents.pythonAgents.evaluations.simple_eval import SimpleEvaluation
from engine.utils.agent_utils import get_legal_moves_for_turn

class Node:
    def __init__(self, board, value, parent=None, id=None):
        self.id = id
        self.board = board
        self.value = value
        self.is_expanded = False
        self.parent = parent
        
        
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
    

class SimpleTreeSearch:
    """
    
    """
    def __init__(self, evaluation=SimpleEvaluation(), max_depth=3, verbose=False):
        self.evaluation = evaluation
        initial_board = chess.Board()
        self.search_tree = SearchTree(initial_board)
        print(self.search_tree)
        self.max_depth = max_depth
        self.nodes_expanded = 0
        self.verbose = verbose
            
    def search(self, board: chess.Board):
        self.search_tree = SearchTree(board)
        self.nodes_visited = 0
        node = Node(board, 0)
        optimal_move, optimal_value = self._search(node, 0)
        
        if self.verbose:
            print('#################### Starting search ####################')
            print(f"Search completed. Search tree size: {len(self.search_tree.nodes)} nodes")#
            print(f"Nodes visited: {self.nodes_visited}")
            print('Duplicates: ', self.search_tree.find_dupes())
            print('#################### Finished search ####################')
        return optimal_move, optimal_value

    def expand_node(self, node, depth, verbose=False):
        
        self.nodes_expanded +=1        
        
        legal_moves = list(get_legal_moves_for_turn(node.board))
        children = []
        
        for move in legal_moves:
            temp_board = deepcopy(node.board)
            temp_board.push(move);
            new_node = Node(board=temp_board, value=0, parent=node)
            self.search_tree.add_node(new_node)
            children.append(new_node)
            
        if verbose:
            print('*'*50)
            print(f'expanding node at depth {depth}:', self.nodes_expanded)
            print(node.board)
            print(f'node expanded with {len(legal_moves)} children')
            print('*'*50)
            
        node.children = children
        
        return
        
    def _search(self, node, depth):
        self.nodes_visited += 1
        if depth == self.max_depth:
            node.value = self.evaluation.evaluate_position(node.board)
            return None, node.value  # No move to associate, only value

        if not node.is_expanded:
            self.expand_node(node, depth)
            node.is_expanded = True

        if not node.children:  # No legal moves, game over or stalemate
            node.value = self.evaluation.evaluate_position(node.board)
            return None, node.value

        best_move = None
        if node.board.turn == 1:  # Maximizing player
            max_value = float('-inf')
            for child in node.children:
                move, value = self._search(child, depth + 1)
                if value > max_value:
                    max_value = value
                    best_move = child.board.move_stack[-1]                  
                
            return best_move, max_value
        else:  # Minimizing player
            min_value = float('inf')
            for child in node.children:
                move, value = self._search(child, depth + 1)
                if value < min_value:
                    min_value = value
                    best_move = child.board.move_stack[-1]
                    
            return best_move, min_value
