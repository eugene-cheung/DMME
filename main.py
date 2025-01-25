from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap

from analyse_game import readPGN, analyseGame

app = Flask(__name__)
Bootstrap(app)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analysis", methods=["POST"])
def analysis():
    pgn_data = request.form['pgn']
    return render_template("analysis.html")
    pgn = readPGN("lichess_pgn_2024.09.05_TigritoForever_vs_shubindani.1Ex3Xcl7 (2).pgn")
    data = analyseGame(pgn)
    print(data)
    return render_template("analysis.html", data = data)

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)