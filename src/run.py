import random

import numpy as np

from display import render
from settings import size

# infinity
INF = float("inf")


def move(grid, row, col, player):
    grid[row][col] = player


def undo(grid, row, col):
    grid[row][col] = 0


def get_user_input(grid):
    while True:
        render(grid)
        print("   ENTER ROW AND COLUMN")
        choice = input("   > ").split()
        try:
            row, col = map(int, choice)
            if row < 0 or col < 0:
                continue
            # computer is represented as 1
            # user is represented as -1
            move(grid, row, col, -1)
            break
        except:
            continue


def win_player(grid, char):
    # check if a player wins the game
    # check for rows, columns and diagonals
    result = char * size in grid.sum(axis=1)
    result = result or char * size in grid.sum(axis=0)
    result = result or char * size == np.trace(grid)
    result = result or char * size == np.trace(np.fliplr(grid))
    return result


def terminal(grid):
    # check if the game is at a terminal state
    # a game is a terminal state if either player wins or it's a tie
    return win_player(grid, -1) or win_player(grid, 1) or 0 not in grid


def utility(grid):
    # return the score corresponding to the terminal state
    if win_player(grid, -1):
        return -1
    if win_player(grid, 1):
        return 1
    return 0


def actions(grid):
    # return possible actions a player can take at each state
    result = np.where(grid == 0)
    result = np.transpose(result)
    np.random.shuffle(result)
    return result


def minimax(grid, computer, alpha, beta, depth):
    # return the maximum value a player can obtain at each step
    if terminal(grid):
        return utility(grid), depth

    if computer:
        func = max
        m = -INF
        char = 1
    else:
        func = min
        m = INF
        char = -1

    for action in actions(grid):
        row, col = action
        move(grid, row, col, char)
        value, depth = minimax(grid, not computer, alpha, beta, depth + 1)
        m = func(m, value)
        # undo the move
        undo(grid, row, col)
        # alpha-beta pruning
        if computer:
            alpha = func(alpha, m)
        else:
            beta = func(beta, m)

        if beta <= alpha:
            break

    return m, depth


def best_move(grid):
    # find all empty cells and compute the minimax for each one
    m = alpha = -INF
    d = beta = INF
    for action in actions(grid):
        row, col = action
        move(grid, row, col, 1)
        value, depth = minimax(grid, False, alpha, beta, 0)
        if value > m or (value == m and depth < d):
            result = row, col
            m = value
            d = depth
        # undo the move
        undo(grid, row, col)
    return result


def game_loop(grid):
    while True:
        # player turn
        get_user_input(grid)
        render(grid)
        # check if the player wins
        if win_player(grid, -1):
            print("   YOU WIN!")
            break
        # check if it's a tie
        if terminal(grid):
            print("   TIE!")
            break
        # computer turn
        row, col = best_move(grid)
        move(grid, row, col, 1)
        render(grid)
        # check if machine wins
        if win_player(grid, 1):
            print("   YOU LOSE!")
            break


def play():
    while True:
        grid = np.zeros((size, size), int)
        game_loop(grid)
        print("   PLAY AGAIN ? [Y/N]")
        again = input("   > ")
        if again.upper() != "Y":
            break


if __name__ == "__main__":
    try:
        play()
    except KeyboardInterrupt:
        print("\n   KEYBOARD INTERRUPT : ABORT")
