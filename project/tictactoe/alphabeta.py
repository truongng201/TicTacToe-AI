"""
TODO: Implement the AlphaBetaPlayer class. The only difference from Minima is the addition of alpha-beta pruning.
* Note: You should read the game logic in project/game.py to familiarize yourself with the environment.
"""
import random
import math
from ..player import Player
from ..game import TicTacToe

class TTT_AlphaBetaPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game: TicTacToe):
        depth = len(game.empty_cells())
        if depth == 0 or game.game_over():
            return
        
        if len(game.empty_cells()) == 9:
            move = random.choice(game.empty_cells())
        else:
            # Alpha-Beta Pruning: Initialize alpha to negative infinity and beta to positive infinity
            alpha = -math.inf
            beta = math.inf
            choice = self.minimax(game, depth, self.letter, alpha, beta)
            move = [choice[0], choice[1]]
        return move

    def minimax(self, game: TicTacToe, depth: int, player_letter: str, alpha: float, beta: float):
        """
        AI function that chooses the best move with alpha-beta pruning.
        :param game: current game state
        :param depth: node index in the tree (0 <= depth <= 9)
        :param player_letter: value representing the player
        :param alpha: best value that the maximizer can guarantee
        :param beta: best value that the minimizer can guarantee
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
                _, _, score = self.minimax(temp_game, depth - 1, "O", alpha, beta)
                
                if score > best_score:
                    best_score = score
                    best = [next_x, next_y, best_score]
                
                # Alpha-Beta Pruning
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best

        if player_letter == "O":
            best_score = math.inf
            best = [None, None, best_score]
            
            for cell in game.empty_cells(state=game.board_state):
                next_x, next_y = cell
                temp_game = game.copy()
                temp_game.set_move(next_x, next_y, player_letter)
                _, _, score = self.minimax(temp_game, depth - 1, "X", alpha, beta)
                
                if score < best_score:
                    best_score = score
                    best = [next_x, next_y, best_score]
                
                # Alpha-Beta Pruning
                beta = min(beta, best_score)
                if beta <= alpha:
                    break

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
        return "Alpha-Beta Player"