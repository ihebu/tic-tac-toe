import os
import random

INFINITY = float("inf")
CLEAR = "clear" if os.name == "posix" else "cls"
SIZE = 3
SEPARATOR = "-" * (4 * SIZE + 1)


def empty():
    # return an empty grid
    return [[" "] * SIZE for i in range(SIZE)]


def shuffled(iter):
    # return a randomly shuffled version of an interable
    iter = list(iter)
    random.shuffle(iter)
    return iter


def render(grid):
    # clear the screen to print at the same place
    os.system(CLEAR)
    print(SEPARATOR)
    for i in range(SIZE):
        print("|", end=" ")
        for j in range(SIZE):
            print(grid[i][j] + " |", end=" ")
        print("\n" + SEPARATOR)


def win_player(grid, char):
    # check if a player wins the game
    # check rows
    for i in range(3):
        if all(grid[i][j] == char for j in range(3)):
            return True
    # check columns
    for j in range(3):
        if all(grid[i][j] == char for i in range(3)):
            return True
    # check diagonals
    if all(grid[i][i] == char for i in range(3)):
        return True
    if all(grid[i][2 - i] == char for i in range(3)):
        return True


def coordinates(choice):
    # return the row and coloumn corresponding to user input
    # get row
    row = 3 - ((choice + 2) // 3)
    # get col
    col = (choice - 1) % 3
    return row, col


def terminal(grid):
    # check if the game is at a terminal state
    # player wins
    if win_player(grid, "X"):
        return True
    # computer wins
    if win_player(grid, "O"):
        return True
    # tie
    if all(grid[i][j] != " " for i in range(3) for j in range(3)):
        return True
    # otherwise the game isn't over yet
    return False


def utility(grid):
    # return the score corresponding to the terminal state
    if win_player(grid, "X"):
        return -1
    if win_player(grid, "O"):
        return 1
    return 0


def actions(grid):
    # return possible actions a player can take at each state
    result = []
    for i in shuffled(range(3)):
        for j in shuffled(range(3)):
            if grid[i][j] == " ":
                result.append((i, j))
    return result


def minimax(grid, computer, alpha, beta, depth):
    # return the maximum value a player can obtain at each step
    if terminal(grid):
        return utility(grid), depth

    if computer:
        func = max
        m = -INFINITY
        char = "O"
    else:
        func = min
        m = INFINITY
        char = "X"

    for action in actions(grid):
        i, j = action
        grid[i][j] = char
        value, depth = minimax(grid, not computer, alpha, beta, depth + 1)
        m = func(m, value)
        # undo the move
        grid[i][j] = " "
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
    m = alpha = -INFINITY
    d = beta = INFINITY
    for action in actions(grid):
        i, j = action
        grid[i][j] = "O"
        value, depth = minimax(grid, False, alpha, beta, 0)
        if value > m or (value == m and depth < d):
            result = i, j
            m = value
            d = depth
        # undo the move
        grid[i][j] = " "
    return result


def get_user_input(grid):
    # ask for player input : a number between 1 and 9
    while True:
        render(grid)
        choice = input()
        # validate input
        if choice not in [str(i) for i in range(1, 10)]:
            continue
        choice = int(choice)
        i, j = coordinates(choice)
        if grid[i][j] != " ":
            continue
        # if cell is not full : fill with 'X'
        grid[i][j] = "X"
        break


def game_loop(grid):
    while True:
        # player turn
        get_user_input(grid)
        render(grid)
        # check if the player wins
        if win_player(grid, "X"):
            print("\nYou win!")
            break
        # check if it's a tie
        if terminal(grid):
            print("\nTie!")
            break
        # computer turn
        # find the best move to play
        i, j = best_move(grid)
        grid[i][j] = "O"
        # display the grid
        render(grid)
        # check if the computer wins with this choice
        if win_player(grid, "O"):
            print("\nYou lose!")
            break


def play():
    while True:
        grid = empty()
        game_loop(grid)
        again = input("Play again ? [y/n] ")
        if again.upper() != "Y":
            break


if __name__ == "__main__":
    try:
        play()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt : Abort")
