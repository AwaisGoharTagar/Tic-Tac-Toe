import streamlit as st
import numpy as np

st.set_page_config(page_title="Tic-Tac-Toe AI", layout="centered")

# Styling for a better UI
def set_custom_css():
    st.markdown(
        """
        <style>
            body { text-align: center; background-color: #f0f0f0; }
            .stButton>button { width: 100px; height: 100px; font-size: 24px; }
            .winner { font-size: 24px; color: green; font-weight: bold; }
            .loser { font-size: 24px; color: red; font-weight: bold; }
            .draw { font-size: 24px; color: orange; font-weight: bold; }
        </style>
        """,
        unsafe_allow_html=True,
    )

set_custom_css()

st.title("⭕ Tic-Tac-Toe ❌")

# Initialize game state if not set
if "board" not in st.session_state:
    st.session_state.board = np.full((3, 3), " ")
    st.session_state.game_over = False
    st.session_state.current_player = "X"

def check_winner(board):
    for i in range(3):
        if board[i, 0] == board[i, 1] == board[i, 2] and board[i, 0] != " ":
            return board[i, 0]
        if board[0, i] == board[1, i] == board[2, i] and board[0, i] != " ":
            return board[0, i]
    
    if board[0, 0] == board[1, 1] == board[2, 2] and board[0, 0] != " ":
        return board[0, 0]
    if board[0, 2] == board[1, 1] == board[2, 0] and board[0, 2] != " ":
        return board[0, 2]
    
    if " " not in board:
        return "Draw"
    return None

def reset_game():
    st.session_state.board = np.full((3, 3), " ")
    st.session_state.game_over = False
    st.session_state.current_player = "X"

def ai_move():
    empty_cells = np.argwhere(st.session_state.board == " ")
    if empty_cells.size > 0:
        ai_choice = empty_cells[np.random.choice(len(empty_cells))]
        st.session_state.board[ai_choice[0], ai_choice[1]] = "O"

# Game Grid
for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        with cols[j]:
            if st.button(st.session_state.board[i, j], key=f"{i}-{j}"):
                if st.session_state.board[i, j] == " " and not st.session_state.game_over:
                    st.session_state.board[i, j] = "X"
                    winner = check_winner(st.session_state.board)
                    if winner:
                        st.session_state.game_over = True
                    else:
                        ai_move()
                        winner = check_winner(st.session_state.board)
                        if winner:
                            st.session_state.game_over = True

# Display winner or draw message
winner = check_winner(st.session_state.board)
if winner:
    if winner == "Draw":
        st.markdown("<p class='draw'>It's a Draw! 🤝</p>", unsafe_allow_html=True)
    else:
        st.markdown(f"<p class='winner'>🎉 {winner} Wins!</p>" if winner == "X" else "<p class='loser'>🤖 AI (O) Wins!</p>", unsafe_allow_html=True)

# Reset button
if st.button("🔄 Restart Game"):
    reset_game()
