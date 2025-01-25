import chess
import chess.pgn
import requests
import json
from stockfish import Stockfish

stockfish = Stockfish(path="stockfish/stockfish-windows-x86-64-avx2.exe")

def readPGN(file):
    # print(file)
    pgn = open(file)
    first_game = chess.pgn.read_game(pgn)
    # print(first_game)
    return first_game

def analyseGame(game):
    # print(game)
    data = []
    board = game.board()
    for move in game.mainline_moves():
        board.push(move)
        stockFishResults = stockfishFile(board.fen(), 5)
        # board, eval, continuation, legal moves
        data.append([board, stockFishResults[0], stockFishResults[1], getLegalMoves(board)])
    
    return data


def getLegalMoves(board):
    return board.legal_moves

# https://stockfish.online/api/s/v2.php
# def stockfishAPI(fen, depth):
#     url = "https://stockfish.online/api/s/v2.php"

#     response = requests.get(url+"?fen="+fen+"&depth=" + str(depth))
#     data = response.json()

#     if data['success'] == False:
#         print("There was an error with stockfish")
#         return

#     return [data['bestmove'], data['evaluation'], data['continuation']]

def stockfishFile(fen, depth):
    stockfish.set_fen_position(fen)
    stockfish.set_depth(depth)
    # stockfish.is_move_correct('a2a3')

    data = [stockfish.get_best_move(), stockfish.get_evaluation()]
    return data

# print(analyseGame(readPGN("lichess_pgn_2024.09.05_TigritoForever_vs_shubindani.1Ex3Xcl7 (2).pgn")))