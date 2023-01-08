def empty_cells_coord(grid):
    empty_cells = []
    for row in range(3):
        for col in range(3):
            if grid[row][col] == "_":
                empty_cells.append((row, col))
    return empty_cells


def evaluate(grid):
    if any(["X" * 3 in "".join(row) for row in grid]):
        return 10
    elif any(["O" * 3 in "".join(row) for row in grid]):
        return -10

    if any([all([grid[i][j] == "X" for i in range(3)]) for j in range(3)]):
        return 10
    elif any([all([grid[i][j] == "O" for i in range(3)]) for j in range(3)]):
        return -10

    if grid[0][0] == grid[1][1] == grid[2][2]:
        if grid[0][0] == "X":
            return 10
        elif grid[0][0] == "O":
            return -10

    if grid[0][2] == grid[1][1] and grid[1][1] == grid[2][0]:
        if grid[0][2] == "X":
            return 10
        elif grid[0][2] == "O":
            return -10
    return 0


def minmax(grid, depth, maximizing):
    score = evaluate(grid)
    if score == 10:
        return score - depth
    if score == -10:
        return score + depth
    if len(empty_cells_coord(grid)) == 0:
        return 0
    if maximizing:
        best = -1000
        empty_cells = empty_cells_coord(grid)
        for x, y in empty_cells:
            grid[x][y] = "X"
            best = max(best, minmax(grid, depth + 1, False))
            grid[x][y] = "_"
        return best
    elif not maximizing:
        best = 1000
        empty_cells = empty_cells_coord(grid)
        for x, y in empty_cells:
            grid[x][y] = "O"
            best = min(best, minmax(grid, depth + 1, True))
            grid[x][y] = "_"
        return best


def find_best_move(grid_, mark):
    empty_cells_ = empty_cells_coord(grid_)
    if mark == "X":
        best_val = -1000
        best_move = None

        for row, col in empty_cells_:
            grid_[row][col] = "X"
            move_val = minmax(grid_, 0, False)
            grid_[row][col] = "_"
            if move_val > best_val:
                best_move = (row, col)
                best_val = move_val
    elif mark == "O":
        best_val = 1000
        best_move = None

        for row, col in empty_cells_:
            grid_[row][col] = "O"
            move_val = minmax(grid_, 0, True)
            grid_[row][col] = "_"
            if move_val < best_val:
                best_val = move_val
                best_move = (row, col)
    # print("The value of the best Move is :", best_val)
    # print()
    # print(best_move)
    return best_move[0] + 1, best_move[1] + 1
