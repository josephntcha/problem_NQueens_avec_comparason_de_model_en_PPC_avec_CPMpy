import cpmpy as cp

from helpers import run_cli


def build_model(n: int) -> cp.Model:
    board = cp.boolvar(shape=(n, n), name="cases")
    constraints = []

    for i in range(n):
        constraints.append(cp.sum(board[i, :]) == 1)
        constraints.append(cp.sum(board[:, i]) == 1)

    for diagonal_sum in range(2 * n - 1):
        cells = [(row, diagonal_sum - row) for row in range(n) if 0 <= diagonal_sum - row < n]
        if len(cells) > 1:
            constraints.append(cp.sum([board[row, col] for row, col in cells]) <= 1)

    for diagonal_difference in range(1 - n, n):
        cells = [(row, diagonal_difference + row) for row in range(n) if 0 <= diagonal_difference + row < n]
        if len(cells) > 1:
            constraints.append(cp.sum([board[row, col] for row, col in cells]) <= 1)

    return cp.Model(constraints)


if __name__ == "__main__":
    run_cli("boolean", build_model)
