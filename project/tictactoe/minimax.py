"""
TODO: Implement the TTT_MinimaxPlayer class.
* Note 1: You should read the game logic in project/game.py to familiarize yourself with the environment.
* Note 2: You don't have to strictly follow the template or even use it at all. Feel free to create your own implementation.
"""

from typing import List, Tuple, Union
import random
import math
from ..player import Player
from ..game import TicTacToe

class TTT_MinimaxPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game: TicTacToe) -> Union[List[int], Tuple[int, int]]:
        depth = len(game.empty_cells())
        
        if depth == 9:
            move = random.choice(list(game.empty_cells())) # Random move if it's the first move
        else:
            move = self.minimax(game, depth, self.letter)
        
        return move

    def minimax(self, game: TicTacToe, depth: int, player_letter: str) -> Union[List[int], Tuple[int, int]]:
        """
        Minimax algorithm that chooses the best move
        :param game: current game state
        :param depth: node index in the tree (0 <= depth <= 9), but never 9 in this case
        :param player_letter: value representing the player
        :return: [row, col, best_score] of the selected move
        """
        if game.game_over() or depth == 0:
            return [None, None, self.evaluate(game)]
        
        best = [None, None, None]
        
        if player_letter == "X":
            best_score = -math.inf
            best = [None, None, best_score]
            
            for cell in game.empty_cells(state=game.board_state):
                next_x, next_y = cell
                temp_game = game.copy()
                temp_game.set_move(next_x, next_y, player_letter)
                _, _, score = self.minimax(temp_game, depth - 1, "O")
                
                if score > best_score:
                    best_score = score
                    best = [next_x, next_y, best_score]
            return best                
            
            
        if player_letter == "O":
            best_score = math.inf
            best = [None, None, best_score]
            
            for cell in game.empty_cells(state=game.board_state):
                next_x, next_y = cell
                temp_game = game.copy()
                temp_game.set_move(next_x, next_y, player_letter)
                _, _, score = self.minimax(temp_game, depth - 1, "X")
                
                if score < best_score:
                    best_score = score
                    best = [next_x, next_y, best_score]
                
            return best
        
        
        return best
    
    def evaluate(self, game: TicTacToe) -> int:
        """
        Function to evaluate the score of game state.
        :param game: the game state to evaluate
        :return: the score of the board from the perspective of current player
        """
        
        if game.wins("X"): 
            return 1
        
        if game.wins("O"): 
            return -1
        
        return 0
    
    def __str__(self) -> str:
        return "Minimax Player"