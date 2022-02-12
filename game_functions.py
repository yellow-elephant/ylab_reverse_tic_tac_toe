from random import choice
import numpy as np


def get_possible_moves(board: list) -> [list, None]:
    moves = list()
    for x in range(10):
        for y in range(10):
            if not board[x][y]:
                moves.append([x, y])
    if moves.__len__() == 0:
        return None
    return moves


def get_ai_move(possible_moves: list) -> [list]:
    return choice(possible_moves)


def change_turn(whose_turn: str) -> str:
    if whose_turn == "X":
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
    if any(pattern in x for x in [row, column, minor_diagonal, major_diagonal]):
        return True
    return False
