import streamlit as st
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional

st.set_page_config(page_title="Tic-Tac-Toe Game", page_icon="🎮", layout="centered")

# ---------------------- Style (Frontend only) ----------------------
st.markdown(
    '<style>'
    '.title {text-align:center; font-size: 50px; font-weight: 700; margin-top: 6px;'
    'position: relative; left: 20px;'
    '}'
    '.subtitle {text-align:center; color:#6b7280; margin-bottom: 12px;}'
    '.board {max-width: 420px; margin: 0 auto;}'
    '.board .stButton>button {height: 130; font-size: 36px; font-weight: 700;}'
    '.topbar {display:flex; gap:10px; justify-content:center; margin: 8px 0 16px;}'
    '.status {text-align:center; font-weight:600; margin: 6px 0 12px;}'
    '.muted {color:#6b7280;}'
    '</style>',
    unsafe_allow_html=True,
)

@dataclass
class GameState:
    board: List[str] # Current state of the board
    turn: str # 'X' or 'O'
    game_over: bool # If the game ends
    status_message: str # 'Winner: X', 'Draw', 'Turn: X'
    scores: Dict[str, int]    # e.g: {'X':int = 3, 'Y':int = 0}

@dataclass
class Settings:
    player1: str # 'Computer' / 'User'
    player2: str
    player1_mode: str # 'User' -> None / 'Computer' -> ['Easy', 'Medium', 'Hard']
    player2_mode: str


# ---------------------- Session bootstrap ----------------------
def init_session():
    if 'settings' not in st.session_state:
        st.session_state.settings = Settings(
            player1='Computer', player2='Computer', player1_mode='Hard', player2_mode='Hard'
        )
    if 'game' not in st.session_state:
        st.session_state.game = GameState(
            board=['']*9, turn='X', game_over=False, status_message='Turn: X',
            scores={'X':0, 'O':0, 'Draw':0}
        )

init_session()

# ---------------------- Hooks ----------------------
def apply_settings_hook(s: Settings):
    pass

def start_game_hook():
    pass

def new_game_hook():
    pass

def reset_scores_hook():
    pass

def cell_click_hook(index: int):
    pass


st.sidebar.header('Settings')

# --- Decision on Player 1 ---
player1_label = st.sidebar.selectbox('Player 1', ['Computer', 'User'], index=0)
player1_mode_val = None
if player1_label == 'Computer':
    player1_mode_val = st.sidebar.radio(
        'Player 1 Difficulty',
        ['Easy', 'Medium', 'Hard'],
        index=0,
        horizontal=True
    )

# --- Decision on Player 2 ---
player2_label = st.sidebar.selectbox('Player 2', ['Computer', 'User'], index=0)
player2_mode_val = None
if player2_label == 'Computer':
    player2_mode_val = st.sidebar.radio(
        'Player 2 Difficulty',
        ['Easy', 'Medium', 'Hard'],
        index=0,
        horizontal=True
    )

# Set new Settings before starting a Game
if st.sidebar.button('Set New Settings'):
    st.session_state.settings = Settings(
        player1=player1_label, player2=player2_label, player1_mode=player1_mode_val, player2_mode=player2_mode_val
    )
    apply_settings_hook(st.session_state.settings)



# Title of the Page
st.markdown("<div class='title'>❌ Tic-Tac-Toe Game ⭕</div>", unsafe_allow_html=True)

# Status Message
st.markdown(f"<div class='status'>{st.session_state.game.status_message}</div>", unsafe_allow_html=True)

# ---------------------- Board ----------------------
def render_cell(i: int):
    label = st.session_state.game.board[i] if st.session_state.game.board[i] else ' '
    def _on_click(idx=i):
        cell_click_hook(idx)
        if not st.session_state.game.game_over:
            if st.session_state.game.board[idx] == '':
                st.session_state.game.board[idx] = st.session_state.game.turn
                st.session_state.game.turn = 'O' if st.session_state.game.turn == 'X' else 'X'
                st.session_state.game.status_message = f"Sıra: {st.session_state.game.turn}"
    st.button(label, key=f'cell_{i}', on_click=_on_click, use_container_width=True)

st.markdown("<div class='board'>", unsafe_allow_html=True)
for r in range(3):
    cols = st.columns(3, gap='small')
    for c in range(3):
        with cols[c]:
            render_cell(r*3+c)

st.markdown("</div>", unsafe_allow_html=True)

st.divider()

colA, colB, colC = st.columns(3)
with colA:
    if st.button('🚀 Start the Game', use_container_width=True):
        start_game_hook()
with colB:
    if st.button('↻ Restart', use_container_width=True):
        new_game_hook()
with colC:
    if st.button('🏁 Reset the Score', use_container_width=True):
        reset_scores_hook()