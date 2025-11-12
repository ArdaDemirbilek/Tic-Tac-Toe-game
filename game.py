from dataclasses import dataclass
from typing import List, Dict, Optional
import random

@dataclass
class Settings:
    player1: str            # "Computer" | "User"
    player2: str
    player1_mode: Optional[str]  # None | "Easy" | "Medium" | "Hard"
    player2_mode: Optional[str]

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

    def start_game(self):
        self.started = True

    def restart_game(self):
        pass

    def reset_scores(self):
        pass