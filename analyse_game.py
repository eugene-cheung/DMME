import chess
import chess.pgn
import requests
import json
from stockfish import Stockfish
from io import StringIO

stockfish = Stockfish(path="stockfish/stockfish-windows-x86-64-avx2.exe")

def readPGN(stringPGN):
    pgn = StringIO(stringPGN)
    return chess.pgn.read_game(pgn)

def analyseGame(game):
    data = []
    board = game.board()
    for move in game.mainline_moves():
        board.push(move)
        stockFishResults = stockfishFile(board.fen(), 5)
        # board, eval, continuation, legal moves
        data.append([board.fen(), stockFishResults[0], stockFishResults[1], getLegalMoves(board)])
    
    return data


def getLegalMoves(board):
    return board.legal_moves

def stockfishFile(fen, depth):
    stockfish.set_fen_position(fen)
    stockfish.set_depth(depth)

    data = [stockfish.get_best_move(), stockfish.get_evaluation()]
    return data

