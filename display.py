import os

size = 3
separator = "-" * (4 * size + 1)
clear = "clear" if os.name == "posix" else "cls"
items = [str(c) for c in range(size)]

guide = """
   TIC-TAC-TOE WITH AI -- HUMAN VS MACHINE
    
   HUMAN : X
   MACHINE : O
"""


def print_cols(grid, i):
    print(f" {i} | ", end="")
    for j in range(size):
        value = grid[i, j]
        char = [" ", "O", "X"][value]
        print(char + " | ", end="")


def print_lines(grid):
    for i in range(size):
        print_cols(grid, i)
        print("\n   " + separator)


def render(grid):
    # clear the screen to print at the same place
    os.system(clear)
    print(guide)
    print("     ", end="")
    print("   ".join(items), end="")
    print("\n   " + separator)
    print_lines(grid)
    print()
