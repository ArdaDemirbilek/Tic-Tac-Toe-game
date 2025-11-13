from dataclasses import dataclass
from typing import List, Dict
import random

@dataclass
class Settings:
    """
    Dataclass to store the game settings (who is user, who is computer,
    which difficulty) in a single data structure
    """
    def __init__(self, player1, player2, player1_mode, player2_mode):
        self.player1: str = player1 # "Computer" | "User"
        self.player2: str = player2
        self.player1_mode: str | None = player1_mode # None | "Easy" | "Medium" | "Hard"
        self.player2_mode: str | None = player2_mode


class Game:
    """
    Main Data structure to store the state and logic of the game. It manages the
    functions required for Game Stream and  is called by Streamlit's main.py file
    """
    def __init__(self, s: Settings):
        # --- settings ---
        self.settings: Settings = s
        # --- state ---
        self.board: List[str] = [''] * 9 # Object to store squared chosen by user and computer
        self.turn: str = 'X' # Whose turn is it
        self.game_over: bool = False # Is Game finished?
        self.started: bool = False # Is Start Game button pressed?
        self.status_message: str = "Press Start" # Gives informative messages about the game
        self.scores: Dict[str, int] = {'X': 0, 'O': 0, 'Draw': 0}


    def start_game(self):
        """
        It gets triggered when Start the Game button is pressed. It changes Game's
        self.started attribute to allow Game Stream to be started
        """
        self.started = True


    def restart_game(self):
        """
        It gets triggered when Restart button is triggered. It changes the state attributes
        to prepare the game for next round
        """
        self.board: List[str] = [''] * 9
        self.turn: str = 'X'
        self.game_over: bool = False
        self.status_message: str = "Press Start"
        self.started: bool = False


    def reset_scores(self):
        """
        It gets triggered when Reset the Score button is pressed. It resets the current score to
        'X': 0, 'O': 0, 'Draw': 0
        """
        self.scores: Dict[str, int] = {'X': 0, 'O': 0, 'Draw': 0}


    def make_move(self, index: int):
        """
        Given the chosen square by the player or the computer the function updates engine.board
        to store the inputs
        :param index: the chosen square by the player
        """
        if self.board[index] == '' and not self.game_over:
            self.board[index] = self.turn
            return True
        return False


    def swap_turn(self):
        """
        It changes the turn of the game: X -> O or O -> X
        """
        self.turn = 'O' if self.turn == 'X' else 'X'
        self.status_message = (f"Sıra: {self.turn} "
            f"({self.settings.player1 if self.turn == 'X' else self.settings.player2})")


    def computer_move(self):
        """
        Considering the difficulty of the computer, the function returns the index,
        the computer wishes to play
        """
        # Find the difficulty of the computer
        player = 'X' if self.turn == 'X' else 'O'
        opponent = 'O' if self.turn == 'X' else 'X'
        player_mode = self.settings.player1_mode if player == 'X' else self.settings.player2_mode

        if player_mode == 'Easy':
            # If the difficulty is easy, computer chose its square randomly
            available_squares = [i for i,j in enumerate(self.board) if j == '']
            chosen_square = random.choice(available_squares)
            return chosen_square

        elif player_mode == 'Medium':
            # If the difficulty is medium, the computer can prevent one-move-losers and
            # don't overlook one-move-winners, otherwise it decides randomly
            def find_critical_move(who_to_check):
                checked_squares = ((0,1,2),(3,4,5),(6,7,8), # rows
                                   (0,3,6),(1,4,7),(2,5,8), # columns
                                   (0,4,8),(2,4,6)) # diagonals

                for i, j, k in checked_squares:
                    line = [self.board[i], self.board[j], self.board[k]]
                    # X '' X | '' X X | X X '' is the scenario to search
                    if line.count(who_to_check) == 2 and line.count('') == 1:
                        if self.board[i] == '': return i
                        if self.board[j] == '': return j
                        if self.board[k] == '': return k
                return None # If nothing can be found

            # Look for a one-move-winner
            winning_move = find_critical_move(player)
            if winning_move is not None:
                return winning_move

            # Look for a one-move-loser
            blocking_move = find_critical_move(opponent)
            if blocking_move is not None:
                return blocking_move

            # Select square randomly
            available_squares = [i for i, j in enumerate(self.board) if j == '']
            if available_squares:
                return random.choice(available_squares)
            return None

        else:
            # --- HARD MODE: SMART MINIMAX (Depth-Weighted) ---
            player_mark = 'X' if self.turn == 'X' else 'O' # for maximizing
            opponent_mark = 'O' if player_mark == 'X' else 'X' # for minimizing

            def check_sim_winner(current_board):
                """
                A helper function which returns the result of the game. Since check_winner is
                a class function, it cannot be used
                """
                winning_combos = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                                  (0, 3, 6), (1, 4, 7), (2, 5, 8),
                                  (0, 4, 8), (2, 4, 6))
                for i, j, k in winning_combos:
                    if current_board[i] == current_board[j] == current_board[k] and current_board[i] != '':
                        return current_board[i]
                if '' not in current_board:
                    return 'Draw'
                return None

            def minimax(board_state, depth, is_maximizing):
                """
                Recursive Minimax algorithm with depth-weighting optimization. It simulates all possible
                future moves to determine the optimal score, prioritizing faster wins and delayed losses.
                :return: The calculated heuristic score for the given board state.
                 """
                result = check_sim_winner(board_state)
                if result == player_mark: return 10 - depth # if current player is winning
                if result == opponent_mark: return -10 + depth # if current player is losing
                if result == 'Draw': return 0 # draw

                if is_maximizing:
                    best_score = -float('inf')
                    for i in range(9):
                        if board_state[i] == '':
                            board_state[i] = player_mark
                            score = minimax(board_state, depth+1, False)
                            board_state[i] = ''
                            best_score = max(score, best_score)
                    return best_score # highest score

                else:
                    best_score = float('inf')
                    for i in range(9):
                        if board_state[i] == '':
                            board_state[i] = opponent_mark
                            score = minimax(board_state, depth+1, True)
                            board_state[i] = ''
                            best_score = min(score, best_score)
                    return best_score # lowest score

            best_final_score = -float('inf')
            best_move = -1
            for i in range(9):
                if self.board[i] == '': # Try possible outcomes if it is available
                    self.board[i] = player_mark
                    move_score = minimax(self.board, 0, False)
                    self.board[i] = '' # After trying turn it back to its previous state
                    if move_score > best_final_score:
                        best_final_score = move_score
                        best_move = i
            return best_move


    def check_winner(self):
        """
        After each move the function checks whether a player managed to win. If a player won or
        no more available squares are left, self.scores are updated accordingly. At the end a Status
        Message is given to inform the user
        """
        checked_squares = ((0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
                           (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
                           (0, 4, 8), (2, 4, 6))  # Diagonals
        winner = None

        # Look whether someone has won
        for squares in checked_squares:
            i, j, k = squares
            # All squares must be equal and not empty
            if self.board[i] != '' and self.board[i] == self.board[j] == self.board[k]:
                winner = self.board[i]  # Winner 'X' or 'O'
                break  # We already found the winner, break the loop

        if winner: # If there is a winner, update the message and score
            self.game_over = True
            self.status_message = f"🏆 Winner: {winner}!"
            self.scores[winner] += 1
            return winner
        elif '' not in self.board: # If there is no winner and the board is full -> Draw:
            self.game_over = True
            self.status_message = "🤝 Draw!"
            self.scores['Draw'] += 1
        return None
