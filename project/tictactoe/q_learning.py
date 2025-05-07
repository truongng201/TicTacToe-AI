from typing import List, Tuple, Union             
from ..player import Player, RandomPlayer
from ..game import TicTacToe
from . import *
from tqdm import tqdm
import numpy as np

NUM_EPISODES = 100000
LEARNING_RATE = 0.5
DISCOUNT_FACTOR = 0.9
EXPLORATION_RATE = 0.1

class TTT_QPlayer(Player):
    def __init__(self, letter, transfer_player=None):
        super().__init__(letter)
        self.opponent = transfer_player
        self.num_episodes = NUM_EPISODES
        self.learning_rate = LEARNING_RATE
        self.gamma = DISCOUNT_FACTOR
        self.epsilon = EXPLORATION_RATE
        self.Q = {}  
        self.action_history = []
    
    def train(self, game):
        """
        Train the Q-Learning player against an transfer player to update the Q tables.
        """
        opponent_letter = 'X' if self.letter == 'O' else 'O'
        if self.opponent is None:
            opponent = TTT_QPlayer(opponent_letter)
        else:
            opponent = self.opponent(opponent_letter)
            
        # using random player
        # opponent = RandomPlayer(opponent_letter)
        print(f"Training Q Player [{self.letter}] for {self.num_episodes} episodes...")
        game_state = game.copy()
        
        for _ in tqdm(range(self.num_episodes)):               
            game_state.restart()
            self.action_history = []
            opponent.action_history = []
            
            current_player = self if self.letter == 'X' else opponent 
            next_player = self if self.letter == 'O' else opponent
            
            while True:                
                if isinstance(current_player, TTT_QPlayer):
                    action = current_player.choose_action(game_state)
                    state = current_player.hash_board(game_state.board_state)
                    current_player.action_history.append((state, action)) 
                else:
                    action = current_player.get_move(game_state)
                
                next_game_state = game_state.copy()
                next_game_state.set_move(action[0], action[1], current_player.letter)
                
                if next_game_state.game_over():
                    reward = 1 if next_game_state.wins(current_player.letter) else -1 if next_game_state.wins(next_player.letter) else 0
                    if isinstance(current_player, TTT_QPlayer):
                        current_player.update_rewards(reward)
                    if isinstance(next_player, TTT_QPlayer):
                        next_player.update_rewards(-reward)
                    break
                else: 
                    current_player, next_player = next_player, current_player
                    game_state = next_game_state    
            
            self.letter = 'X' if self.letter == 'O' else 'O'
            opponent.letter = 'X' if opponent.letter == 'O' else 'O'        
    
    def update_rewards(self, reward: float):
        """
        Update Q-values for all state-action pairs in the action history using the final reward.
        """
        for state, action in reversed(self.action_history):
            next_state = state  # For terminal state, s' = s
            self.update_q_values(state, tuple(action), next_state, reward)
            reward = reward * self.gamma  # Decay reward as we go backward in time
            

    def choose_action(self, game: TicTacToe) -> Union[List[int], Tuple[int, int]]:
        """
        Choose action with ε-greedy strategy.
        if random number < ε, choose random action
        else choose action with the highest Q-value
        """
        possible_actions = game.empty_cells()
        state = self.hash_board(game.board_state)

        # Exploration
        if np.random.rand() < self.epsilon:
            return possible_actions[np.random.randint(len(possible_actions))]

        # Exploitation
        q_values = []
        for action in possible_actions:
            action_tuple = tuple(action)
            q_values.append(self.Q.get((state, action_tuple), 0))

        max_q = max(q_values)
        best_actions = [a for a, q in zip(possible_actions, q_values) if q == max_q]
        return best_actions[np.random.randint(len(best_actions))]
    
    def update_q_values(self, state, action, next_state, reward):
        """
        Given (s, a, s', r), update the Q-value for the state-action pair (s, a) using the Bellman equation:
            Q(s, a) = Q(s, a) + alpha * (reward + gamma * max(Q(s', a')) - Q(s, a))
        """
        curr_q = self.Q.get((state, action), 0)
        # Estimate max future Q value from next state
        next_qs = [self.Q.get((next_state, tuple(a)), 0) for a in [(i, j) for i in range(3) for j in range(3)]]
        max_next_q = max(next_qs) if next_qs else 0

        # Q-learning update rule
        new_q = curr_q + self.learning_rate * (reward + self.gamma * max_next_q - curr_q)
        self.Q[(state, action)] = new_q   
            
        
    def hash_board(self, board):
        """
        Convert board state to a string key for Q-table.
        """
        key = ''
        for i in range(3):
            for j in range(3):
                if board[i][j] == 'X':
                    key += '1'
                elif board[i][j] == 'O':
                    key += '2'
                else:
                    key += '0'
        return key

    def get_move(self, game: TicTacToe):
        """
        Get move during actual play (with no exploration).
        """
        self.epsilon = 0  # No exploration during actual play
        move = self.choose_action(game)
        return move
    
    def __str__(self):
        return "Q-Learning Player"