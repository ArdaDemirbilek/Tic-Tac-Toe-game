# 🎮 Tic-Tac-Toe Game (Streamlit)

Implemented a web-based Tic-Tac-Toe game using Python and **Streamlit**, featuring multiple AI difficulty levels (random, heuristic, and **Minimax with depth weighting**), persistent scoreboard, and configurable player settings.
---

## 🚀 Features

* 🤖 Flexible Play Modes: Play against the AI (User vs Computer), watch the AI battle itself (Computer vs Computer), or play with a friend (User vs User).
* 🧠 Multiple AI Difficulty Levels: Easy (Random), Medium (Heuristic), and Hard (Unbeatable Minimax)
* 🏆 **Score tracking**

  * Player X wins
  * Player O wins
  * Draws
* 🔄 **Restart** button
* ♻️ **Reset Score** functionality
* 🎨 Modern, centered UI layout

---

## 🖼️ Preview

<img width="1874" height="737" alt="image" src="https://github.com/user-attachments/assets/3304ce03-5636-47bf-9072-82b52ff3a250" />

---

## 🧩 Project Structure

```
project/
│
├── main.py        # Streamlit UI, layout, board rendering
├── game.py        # Game logic, move handling, winner detection
└── README.md      # This file
```

---

## 🛠️ Installation & Running

### 1. Install dependencies

```
pip install streamlit
```

### 2. Run the app

```
streamlit run main.py
```

The application will open automatically in your browser.

---

## ♟️ Game Logic

* The game runs on a 3×3 board.
* Each move is processed automatically by the game logic.
* After each move, the program checks for:

  * X win
  * O win
  * Draw
* When the game ends, the board is locked until restarted.

---

## 🤝 Contributing

Pull requests are welcome! Feel free to open an issue for any bug or suggestion.

---

Enjoy the game, and feel free to extend it with new features! 🚀
