import os

from settings import size


SEPARATOR = "-" * (4 * size + 1)

GUIDE = """
   TIC-TAC-TOE WITH AI -- HUMAN VS MACHINE
    
   HUMAN : X
   MACHINE : O
"""

CLEAR = "clear" if os.name == "posix" else "cls"


def _print_cols(grid, i):
    print(f" {i} | ", end="")
    for j in range(size):
        value = grid[i, j]
        char = [" ", "O", "X"][value]
        print(char + " | ", end="")


def _print_lines(grid):
    print("\n   " + SEPARATOR)
    for i in range(size):
        _print_cols(grid, i)
        print("\n   " + SEPARATOR)


def render(grid):
    # clear the screen to print at the same place
    os.system(CLEAR)
    print(GUIDE)
    print("     ", end="")
    for col in range(size):
        print(col, end="   ")
    _print_lines(grid)
    print()
