from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

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
        return render_template("board.html", player=session["player"], board=session["board"])
    else:
        if session["turn"] != session["player"]:
            session["board"] = get_ai_move(session["board"], session["turn"])
        return render_template("board.html", player=session["player"], board=session["board"])


@app.route("/choose/<string:player>")
def choose(player):
    session["player"] = player
    return redirect(url_for("index"))


@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    session["board"][row][col] = session["player"]
    return redirect(url_for("index"))


def get_ai_move(board, turn):
    return board


if __name__ == '__main__':
    app.run()
