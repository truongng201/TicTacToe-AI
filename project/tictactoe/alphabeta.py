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
        opponent = "X" if player_letter == "O" else "O"
        
        if game.game_over() or depth == 0:
            return [-1, -1, self.evaluate(game)]
        
        if player_letter == self.letter:
            best_score = -math.inf
            best = [-1, -1, best_score]
            for cell in game.empty_cells(state=game.board_state):
                next_x, next_y = cell
                temp_game = game.copy()
                temp_game.set_move(next_x, next_y, player_letter)
                _, _, score = self.minimax(temp_game, depth - 1, opponent, alpha, beta)
                
                if score > best_score:
                    best_score = score
                    best = [next_x, next_y, best_score]
                
                # Alpha-Beta Pruning
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best
        else:
            best_score = math.inf
            best = [-1, -1, best_score]
            for cell in game.empty_cells(state=game.board_state):
                next_x, next_y = cell
                temp_game = game.copy()
                temp_game.set_move(next_x, next_y, player_letter)
                _, _, score = self.minimax(temp_game, depth - 1, opponent, alpha, beta)
                
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
        if game.wins(self.letter):
            return 1
        
        opponent = "X" if self.letter == "O" else "O"
        if game.wins(opponent):
            return -1
        
        return 0
    
    def __str__(self) -> str:
        return "Alpha-Beta Player"