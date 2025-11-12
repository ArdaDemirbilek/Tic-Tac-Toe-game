from dataclasses import dataclass
from typing import List, Dict, Optional
import random

@dataclass
class Settings:
    def __init__(self, player1, player2, player1_mode, player2_mode):
        self.player1: str = player1 # "Computer" | "User"
        self.player2: str = player2
        self.player1_mode: str | None = player1_mode # None | "Easy" | "Medium" | "Hard"
        self.player2_mode: str | None = player2_mode

class Game:
    def __init__(self, s: Settings):
        self.settings: Settings = s
        # --- state ---
        self.board: List[str] = [''] * 9
        self.turn: str = 'X'
        self.game_over: bool = False
        self.status_message: str = "Press Start"
        self.scores: Dict[str, int] = {'X': 0, 'O': 0, 'Draw': 0}
        self.started: bool = False

    # (+)
    def start_game(self):
        self.started = True

    # (+)
    def restart_game(self):
        self.board: List[str] = [''] * 9
        self.turn: str = 'X'
        self.game_over: bool = False
        self.status_message: str = "Press Start"
        self.started: bool = False

    # (+)
    def reset_scores(self):
        self.scores: Dict[str, int] = {'X': 0, 'O': 0, 'Draw': 0}

    # (+)
    def make_move(self, index: int):
        """
        Given the chosen square by the player the function updates engine.board to store the inputs
        :param index: the chosen square by the player
        :return:
        """
        if self.board[index] == '' and not self.game_over:
            self.board[index] = self.turn
            return True
        return False

    # (+)
    def swap_turn(self):
        """
        Change the turn of the game: X -> O or O -> X
        :return: None
        """
        self.turn = 'O' if self.turn == 'X' else 'X'
        self.status_message = (f"Sıra: {self.turn} "
            f"({self.settings.player1 if self.turn == 'X' else self.settings.player2})")

    # (+-)
    def computer_move(self):
        available_squares = [i for i,j in enumerate(self.board) if j == '']
        chosen_square = random.choice(available_squares)
        return chosen_square

    # (+)
    def check_winner(self):
        checked_squares = ((0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
                           (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
                           (0, 4, 8), (2, 4, 6))  # Diagonals

        winner = None

        # Look whether someone has won
        for squares in checked_squares:
            i, j, k = squares
            # All sqaures must be equal and not empty
            if self.board[i] != '' and self.board[i] == self.board[j] == self.board[k]:
                winner = self.board[i]  # Winner 'X' or 'O'
                break  # We already found the winner, break teh loop

        if winner:
            # If there is a winner, update the message and score
            self.game_over = True
            self.status_message = f"🏆 Winner: {winner}!"
            self.scores[winner] += 1

        elif '' not in self.board:
            # If there is no winner and the board is full -> Draw:
            self.game_over = True
            self.status_message = "🤝 Draw!"
            self.scores['Draw'] += 1
