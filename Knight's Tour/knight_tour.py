# Author Names: Isabella Stephens, Sosan Wahid, Andrew Kivrak
# Created: 23 November 2022
# Updated: 12 December 2022

import datetime

# checks to see if area on the board exists
def isSafe(x, y, board):
    if 0 <= x < n and 0 <= y < n and board[x][y] == -1:
        return True
    return False

# saves solution to .txt file
# ONLY SAVES 1 KNIGHT TOUR CURRENTLY
def saveSolution(n, board):
    with open('knight_tour_file.txt', 'w') as testfile:  # the w overwrites any other solution; will need to change that
        for row in board:
            testfile.write(' '.join([str(a) for a in row]) + '\n')

        testfile.write('\n')  # final large space


def solveKT(n, x, y):
    # Initialization of Board matrix
    board = [[-1 for i in range(n)] for i in range(n)]

    # move_x and move_y define next movement of Knight.
    move_x = [2, 1, -1, -2, -2, -1, 1, 2]
    move_y = [1, 2, 2, 1, -1, -2, -2, -1]

    board[x][y] = 0  # the starting position will ALWAYS be 0

    # Step counter for knight's position
    pos = 1

    # Checking if solution exists or not
    if not solveKTUtil(n, board, 0, 0, move_x, move_y, pos):
        print("Solution does not exist")
    else:
        saveSolution(n, board)


def solveKTUtil(n, board, curr_x, curr_y, move_x, move_y, pos):
    if pos == n ** 2:
        return True

    # Try all next moves from the current coordinate x, y
    for i in range(8):
        new_x = curr_x + move_x[i]
        new_y = curr_y + move_y[i]
        if isSafe(new_x, new_y, board):
            board[new_x][new_y] = pos
            if solveKTUtil(n, board, new_x, new_y, move_x, move_y, pos + 1):
                return True

            board[new_x][new_y] = -1
    return False


if __name__ == "__main__":
    n = int(input("N = "))
    if n % 2 != 0:  # if n isn't even, just add 1
        n = n + 1

    x = int(input("X = "))
    y = int(input("Y = "))

    print(f'The board is {n} x {n}, x = {x}, y = {y}')
    startTime = datetime.datetime.now()

    if not x > n and y > n:
        # ONLY DOES ONE KNIGHT'S TOUR CURRENTLY
        solveKT(n, x, y)  # actually begin solving
    else:
        print("x or y is too big for board")
    endtime = datetime.datetime.now() - startTime
    print()
    print(endtime)
