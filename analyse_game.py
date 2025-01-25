import chess
import chess.pgn
import requests
import json


def readPGN(file):
    pgn = open(file)
    first_game = chess.pgn.read_game(pgn)
    return first_game

def analyseGame(game):
    data = []
    board = game.board()
    for move in game.mainline_moves():
        board.push(move)
        stockFishResults = stockfishAPI(board.fen(), 12)
        # board, eval, continuation, legal moves
        data.append([board, stockFishResults[1], stockFishResults[2], getLegalMoves(board)])
    
    return data


def getLegalMoves(board):
    return board.legal_moves

# https://stockfish.online/api/s/v2.php
def stockfishAPI(fen, depth):
    url = "https://stockfish.online/api/s/v2.php"

    response = requests.get(url+"?fen="+fen+"&depth=" + str(depth))
    data = response.json()

    if data['success'] == False:
        print("There was an error with stockfish")
        return

    return [data['bestmove'], data['evaluation'], data['continuation']]