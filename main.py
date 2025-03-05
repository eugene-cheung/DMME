from flask import Flask, render_template, request, redirect, url_for, session
from flask_bootstrap import Bootstrap
import chess
import chess.svgo
from phoenix_openai_rag_agent import analyze_game

from analyse_game import readPGN, analyseGame

app = Flask(__name__)
app.secret_key = "your_secret_key"
Bootstrap(app)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analysis", methods=["POST"])
def analysis():
    pgn_data = request.form['pgn']
    pgn = readPGN(pgn_data)
    data = analyseGame(pgn)

    session['game_data'] = data
    session['move_index'] = 0  # Initialize the move index at the first move
    session['match_pgn'] = pgn_data

    board = chess.Board(data[0][0])
    svg_board = chess.svg.board(
        board,
        size=350,
    )
    response = analyze_game(pgn_data, 0)

    return render_template("analysis.html", svg_board=svg_board, response=response)

@app.route("/move", methods=["POST"])
def move():
    move_direction = request.form['direction']  # 'forward' or 'back'
    game_data = session.get('game_data')
    move_index = session.get('move_index', 0)
    match_pgn = session.get('match_pgn')


    if move_direction == 'forward' and move_index < len(game_data) - 1:
        move_index += 1
    elif move_direction == 'back' and move_index > 0:
        move_index -= 1

    # Update the current move in session
    session['move_index'] = move_index

    # Get the FEN for the current move
    board = chess.Board(game_data[move_index][0])
    svg_board = chess.svg.board(
        board,
        size=350,
    )
    response = analyze_game(match_pgn, move_index)

    return render_template("analysis.html", svg_board=svg_board, response=response)

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)