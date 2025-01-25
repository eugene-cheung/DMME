# File for functions for chess python library. 

import chess
import chess.pgn

board = chess.Board()


# Reads a game from a file opened in text.
pgn = open("data/pgn/kasparov-deep-blue-1997.pgn")

first_game = chess.pgn.read_game(pgn)
second_game = chess.pgn.read_game(pgn)

first_game.headers["Event"]
'IBM Man-Machine, New York USA'

# Iterate through all moves and play them on a board.
board = first_game.board()
for move in first_game.mainline_moves():
    board.push(move)

board
board('4r3/6P1/2p2P1k/1p6/pP2p1R1/P1B5/2P2K2/3r4 b - - 0 45')