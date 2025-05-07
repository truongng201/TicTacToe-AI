"""
TODO: Implement the TreeNode for TTT_MCTSPlayer class.
* Note 1: You should read the game logic in project/game.py to familiarize yourself with the environment.
* Note 2: You don't have to strictly follow the template or even use it at all. Feel free to create your own implementation.
"""

import numpy as np
import math
import random

from ..player import Player
from ..game import TicTacToe

WIN = 1
LOSE = -1
DRAW = 0
NUM_SIMULATIONS = 5000
EXPLORATION_CONSTANT = math.sqrt(2)

class TreeNode():
    def __init__(self, game_state: TicTacToe, player_letter: str, parent=None, parent_action=None):
        self.player = player_letter
        self.game_state = game_state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self.N = 0
        self.Q = 0
    
    def select(self) -> 'TreeNode':
        """
        Select the best child node based on UCB1 formula. Keep selecting until a leaf node is reached.
        """
        current_node = self
        while not current_node.is_leaf_node():
            current_node = current_node.best_child()
        return current_node
    
    def expand(self) -> 'TreeNode':
        """
        Expand the current node by adding all possible child nodes. Return one of the child nodes for simulation.
        """
        if self.is_terminal_node():
            return self
            
        for cell in self.game_state.empty_cells():
            x, y = cell
            temp_game = self.game_state.copy()
            temp_game.set_move(x, y, self.game_state.curr_player)
            next_player = 'O' if self.player == 'X' else 'X'
            child_node = TreeNode(
                game_state=temp_game,
                player_letter=next_player,
                parent=self,
                parent_action=(x, y)
            )
            self.children.append(child_node)
        
        return random.choice(self.children)
    
    def simulate(self) -> int:
        """
        Run simulation from the current node until the game is over. Return the result of the simulation.
        """
        sim_game = self.game_state.copy()
        
        while not sim_game.game_over():
            empty_cells = sim_game.empty_cells()
            if not empty_cells:
                break
            x, y = random.choice(empty_cells)
            sim_game.set_move(x, y, sim_game.curr_player)
        
        if sim_game.wins(self.player):
            return WIN
        
        if sim_game.wins('O' if self.player == 'X' else 'X'):
            return LOSE
        
        return DRAW
    
    def backpropagate(self, result: int):
        """
        Backpropagate the result of the simulation to the root node.
        """
        self.N += 1
        self.Q += result
        
        if self.parent is not None:
            self.parent.backpropagate(-result)

            
    def is_leaf_node(self) -> bool:
        return len(self.children) == 0
    
    def is_terminal_node(self) -> bool:
        return self.game_state.game_over()
    
    def best_child(self) -> 'TreeNode':
        return max(self.children, key=lambda c: c.ucb())
    
    def ucb(self, c=EXPLORATION_CONSTANT) -> float:
        if self.N == 0:
            return float('inf')
        return self.Q / self.N + c * np.sqrt(np.log(self.parent.N) / self.N)
    
class TTT_MCTSPlayer(Player):
    def __init__(self, letter, num_simulations=NUM_SIMULATIONS):
        super().__init__(letter)
        self.num_simulations = num_simulations
        self.exploration_constant = EXPLORATION_CONSTANT
    
    def get_move(self, game):
        mcts = TreeNode(game, self.letter)
        for _ in range(self.num_simulations):
            leaf = mcts.select()
            if not leaf.is_terminal_node():
                leaf.expand()
            # Default simulation starts from an expanded node of leaf. However, we can also start simulation from leaf itself to avoid complicating the code.
            result = leaf.simulate() 
            leaf.backpropagate(-result) # Negate the result because it's from the perspective of the opponent
            
        best_child = max(mcts.children, key=lambda c: c.N)
        return best_child.parent_action
    
    def __str__(self) -> str:
        return "MCTS Player"