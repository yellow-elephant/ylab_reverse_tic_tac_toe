from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
from game_functions import *

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
        initialize_session()
    if not get_possible_moves(session["board"]):
        session["draw"] = True
    elif session["whose_turn"] != session["player"]:
        play_ai_turn()
    return render_template("board.html", **session)


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


@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))


def initialize_session():
    session["whose_turn"] = "X"
    session["board"] = list()
    session["draw"] = False
    for x in range(10):
        session["board"].append(list())
        for y in range(10):
            session["board"][x].append(None)
    session["lose"] = False
    session["loser"] = ""


def play_ai_turn():
    move = get_ai_move(get_possible_moves(session["board"]))
    session["board"][move[0]][move[1]] = session["whose_turn"]
    if game_is_lost(session["board"], move, session["whose_turn"]):
        session["lose"] = True
        session["loser"] = "Ai"
    session["whose_turn"] = change_turn(session["whose_turn"])


if __name__ == '__main__':
    app.run()
