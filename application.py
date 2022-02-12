from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
from random import choice
import numpy as np

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    if "player" not in session:
        return render_template('choose_player.html')
    if "board" not in session:
        session["whose_turn"] = "X"
        session["board"] = list()
        for x in range(10):
            session["board"].append(list())
            for y in range(10):
                session["board"][x].append(None)
        session["lose"] = False
        session["loser"] = ""
    if session["whose_turn"] != session["player"]:
        move = get_ai_move(session["board"])
        session["board"][move[0]][move[1]] = session["whose_turn"]
        if game_is_lost(session["board"], move, session["whose_turn"]):
            session["lose"] = True
            session["loser"] = "Ai"
        session["whose_turn"] = change_turn(session["whose_turn"])
    return render_template("board.html", player=session["player"], board=session["board"], lose=session["lose"],
                           loser=session["loser"])


@app.route("/choose/<string:player>")
def choose(player):
    session["player"] = player
    return redirect(url_for("index"))


@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    session["board"][row][col] = session["player"]
    if game_is_lost(session["board"], [row, col], session["whose_turn"]):
        session["lose"] = True
        session["loser"] = "Player"
        return redirect(url_for("index"))
    session["whose_turn"] = change_turn(session["whose_turn"])
    return redirect(url_for("index"))


def get_possible_moves(board: list):
    moves = list()
    for x in range(10):
        for y in range(10):
            if not board[x][y]:
                moves.append([x, y])
    return moves


def get_ai_move(board: list):
    return choice(get_possible_moves(board))


def change_turn(turn: str):
    if turn == "X":
        return "Y"
    else:
        return "X"


def game_is_lost(board: list, move: list, turn: str) -> bool:
    pattern = turn * 5
    arr = np.array(board)
    row = ''.join(str(cell) for cell in arr[move[0]])
    column = ''.join(str(cell) for cell in arr[:, move[1]])
    major_diagonal = ''.join(str(cell) for cell in arr.diagonal(offset=move[1] - move[0]))
    minor_diagonal = ''.join(
        str(cell) for cell in np.diagonal(np.rot90(arr), offset=-arr.shape[1] + (move[0] + move[1]) + 1))
    if pattern in row or pattern in column or pattern in major_diagonal or pattern in minor_diagonal:
        return True
    return False


# def get_diagonals:


if __name__ == '__main__':
    app.run()
