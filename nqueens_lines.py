import cpmpy as cp

from helpers import run_cli


def build_model(n: int) -> cp.Model:
    queens = cp.intvar(0, n - 1, shape=n, name="q")
    return cp.Model(
        cp.AllDifferent(queens),
        cp.AllDifferent([queens[i] + i for i in range(n)]),
        cp.AllDifferent([queens[i] - i for i in range(n)]),
    )


if __name__ == "__main__":
    run_cli("lines", build_model)
