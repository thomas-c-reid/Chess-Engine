import sys

sys.dont_write_bytecode = True

import pytest
import chess
from engine.agents.searchTree.simpleTreeSearch import SimpleTreeSearch

def test_perft():
    
    depth_mappings = [
        {'depth': 1, 'nodes': 20}, 
        {'depth': 2, 'nodes': 400},
        {'depth': 3, 'nodes': 8902},
        {'depth': 4, 'nodes': 197281},
        # {'depth': 5, 'nodes': 4865609}
        ]
    
    total_nodes = 0
        
    for depth_mapping  in depth_mappings:
        total_nodes += depth_mapping['nodes']
        board = chess.Board()
        simple_tree_search = SimpleTreeSearch(max_depth=depth_mapping['depth'])
        simple_tree_search.search(board)
        
        assert len(simple_tree_search.search_tree.nodes) == total_nodes