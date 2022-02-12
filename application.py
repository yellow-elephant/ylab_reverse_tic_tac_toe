from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
from random import choice

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    if "player" not in session:
        return render_template('choose_player.html')
    elif "board" not in session:
        session["turn"] = "X"
        session["board"] = list()
        for x in range(10):
            session["board"].append(list())
            for y in range(10):
                session["board"][x].append(None)
    if session["turn"] != session["player"]:
        session["board"] = get_ai_move(session["board"], session["turn"])
        session["turn"] = change_turn(session["turn"])
    return render_template("board.html", player=session["player"], board=session["board"])


@app.route("/choose/<string:player>")
def choose(player):
    session["player"] = player
    return redirect(url_for("index"))


@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    session["board"][row][col] = session["player"]
    session["turn"] = change_turn(session["turn"])
    return redirect(url_for("index"))


def get_possible_moves(board: list):
    moves = list()
    for x in range(10):
        for y in range(10):
            if not board[x][y]:
                moves.append((x, y))
    return moves


def get_ai_move(board: list, turn: str):
    move = choice(get_possible_moves(board))
    board[move[0]][move[1]] = turn
    return board


def change_turn(turn: str):
    if turn == "X":
        return "Y"
    else:
        return "X"


if __name__ == '__main__':
    app.run()
