from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)


session_dir = mkdtemp()
print(f"Session files are stored in: {session_dir}")

app.config["SESSION_FILE_DIR"] = session_dir
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def check_winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            return board[i][0]  # Winner in row
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
            return board[0][i]  # Winner in column

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]  # Winner in main diagonal
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]  # Winner in anti-diagonal

    return None  # No winner yet

@app.route("/")
def index():
  if "board" not in session:
    session["board"] = [[None, None, None],[None, None, None],[None, None, None]]
    session["turn"] = "X"
    session["winner"] = ""
  return render_template("game.html", game=session["board"], turn=session["turn"], winner=session["winner"])
  

@app.route("/play/<int:row>/<int:col>")
def play(row, col):
  session["board"][row][col] = session["turn"]

  winner = check_winner(session["board"])
  if winner:
    session["winner"] = winner 
  else:
    session["turn"] = 'O' if session["turn"] == 'X' else 'X'

  return redirect(url_for("index"))
  

@app.route("/reset")
def reset():
  # session["board"] = [[None, None, None],[None, None, None],[None, None, None]]
  # session["turn"] = "X"
  # session["winner"] = ""
  session.clear()

  # return render_template("game.html", game=session["board"], turn=session["turn"], winner=session["winner"])
  return redirect(url_for("index")) 