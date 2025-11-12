from time import sleep
import streamlit as st
import game


st.set_page_config(page_title="Tic-Tac-Toe Game", page_icon="🎮", layout="centered")

# ---------------------- Style (Frontend only) ----------------------
st.markdown(
    '<style>'
    '.title {text-align:center; font-size: 50px; font-weight: 700; margin-top: 6px;'
    'position: relative; left: 20px;'
    '}'
    '.subtitle {text-align:center; color:#6b7280; margin-bottom: 12px;}'
    '.board {max-width: 420px; margin: 0 auto;}'
    '.board .stButton>button {height: 130px; font-size: 36px; font-weight: 700;}'
    '.topbar {display:flex; gap:10px; justify-content:center; margin: 8px 0 16px;}'
    '.status {text-align:center; font-weight:600; margin: 6px 0 12px;}'
    '.muted {color:#6b7280;}'
    '</style>',
    unsafe_allow_html=True,
)

# ---------------------- Session bootstrap ----------------------
if "engine" not in st.session_state:
    st.session_state.engine = game.Game(game.Settings(
        player1='Computer', player2='Computer', player1_mode='Easy', player2_mode='Easy'))
    # Default settings: Computer (Easy) vs Computer (Easy)
engine: game.Game = st.session_state.engine # engine variable is a pointer to the st.session_state.engine

player_dict = {'X': engine.settings.player1, 'O': engine.settings.player2}


# ---------------------- Sidebar - Settings ----------------------
st.sidebar.header('Settings')

# If game already started and not finished -> Lock the Settings Section
settings_locked = engine.started and not engine.game_over

# --- Decision on Player 1 ---
player1_label = st.sidebar.selectbox('Player 1', ['Computer', 'User'], index=0, disabled=settings_locked)
player1_mode_val = None
if player1_label == 'Computer':
    player1_mode_val = st.sidebar.radio(
        'Player 1 Difficulty',
        ['Easy', 'Medium', 'Hard'],
        index=0,
        horizontal=True,
        disabled=settings_locked
    )

# --- Decision on Player 2 ---
player2_label = st.sidebar.selectbox('Player 2', ['Computer', 'User'], index=0, disabled=settings_locked)
player2_mode_val = None
if player2_label == 'Computer':
    player2_mode_val = st.sidebar.radio(
        'Player 2 Difficulty',
        ['Easy', 'Medium', 'Hard'],
        index=0,
        horizontal=True,
        disabled=settings_locked
    )

# Set new Settings before starting a Game
if st.sidebar.button('Set New Settings', disabled=settings_locked):
    engine.settings = game.Settings(
        player1=player1_label, player2=player2_label, player1_mode=player1_mode_val, player2_mode=player2_mode_val
    )


# Title of the Page
st.markdown("<div class='title'>❌ Tic-Tac-Toe Game ⭕</div>", unsafe_allow_html=True)

# Status Message
st.markdown(f"<div class='status'>{engine.status_message}</div>", unsafe_allow_html=True)

# ---------------------- Board ----------------------
def render_cell(i: int):
    """
    Renders the board buttons, and checks whether they have been pressed
    :return: True if it is pressed by the User, False if it is not
    """
    label = engine.board[i] if engine.board[i] else ' '
    turn = engine.turn
    is_user = True if 'User' == player_dict[turn] else False
    # If game did not start, or did already end, or it is not user's turn
    # or the button is pressed already -> make the button disable
    clicked = st.button(label, key=f'cell_{i}',
                  disabled = (not engine.started) or engine.game_over
                             or (not is_user) or (engine.board[i] != ''),
                  use_container_width=True)
    return clicked # Pressed or not


st.markdown("<div class='board'>", unsafe_allow_html=True)
for r in range(3):
    cols = st.columns(3, gap='small')
    for c in range(3):
        with cols[c]:
            cell_index = r * 3 + c # The index of a button
            # If a button is pressed, then call necessary engine functions to process the move
            if render_cell(cell_index):
                engine.make_move(cell_index)
                engine.check_winner()
                if not engine.game_over:
                    engine.swap_turn()
                # To make differences visible we need to rerun in order to render again
                st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

st.divider()
colA, colB, colC = st.columns(3)
with colA:
    if st.button(
        '🚀 Start the Game',
        use_container_width=True,
        disabled=engine.started and not engine.game_over
    ):
        # Call start_game() function to prepare the game to be played
        engine.start_game(); st.rerun()
with colB:
    if st.button(
        '↻ Restart',
        use_container_width=True,
        disabled=engine.started and not engine.game_over
    ):
        # Call restart_game() function to clean the board and previous turns highlights
        engine.restart_game(); st.rerun()
with colC:
    if st.button(
        '🏁 Reset the Score',
        use_container_width=True,
        disabled=engine.started and not engine.game_over
    ):
        # Call reset_scores() function, which set the scores back to {'X': 0, 'O': 0, 'Draw': 0}
        engine.reset_scores(); st.rerun()

# ------------- Game Stream -------------
current_player_type = player_dict[engine.turn] # For checking if it's computer's turn
if engine.started and not engine.game_over and current_player_type == 'Computer':
    move_index = engine.computer_move() # Which index the computer chooses
    engine.make_move(move_index) # Update self.board accordingly
    engine.check_winner() # Check the status of the game
    if not engine.game_over:
        engine.swap_turn()
    sleep(0.5) # A short wait
    st.rerun()
