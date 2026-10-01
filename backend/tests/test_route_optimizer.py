from app.services.route_optimizer import (
    EXHAUSTIVE_LIMIT,
    solve_exhaustive,
    solve_tsp,
)


def test_exhaustive_opens_tsp_minimizes_distance():
    matrix = [
        [0.0, 1.0, 2.0, 3.0],
        [1.0, 0.0, 1.0, 2.0],
        [2.0, 1.0, 0.0, 1.0],
        [3.0, 2.0, 1.0, 0.0],
    ]
    assert solve_exhaustive(matrix) == [0, 1, 2, 3]


def test_solve_small_visits_all_exactly_once():
    matrix = [
        [0.0, 5.0, 2.0, 8.0],
        [5.0, 0.0, 3.0, 1.0],
        [2.0, 3.0, 0.0, 4.0],
        [8.0, 1.0, 4.0, 0.0],
    ]
    path = solve_tsp(matrix)
    assert path[0] == 0
    assert sorted(path) == [0, 1, 2, 3]


def test_solve_deterministic():
    matrix = [
        [0.0, 5.0, 2.0, 8.0, 1.0, 3.0],
        [5.0, 0.0, 3.0, 1.0, 4.0, 2.0],
        [2.0, 3.0, 0.0, 4.0, 6.0, 1.0],
        [8.0, 1.0, 4.0, 0.0, 2.0, 5.0],
        [1.0, 4.0, 6.0, 2.0, 0.0, 3.0],
        [3.0, 2.0, 1.0, 5.0, 3.0, 0.0],
    ]
    assert solve_tsp(matrix) == solve_tsp(matrix)


def _synthetic_matrix(n_nodes, seed):
    import random

    rng = random.Random(seed)
    size = n_nodes + 1
    matrix = [[0.0] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if i != j:
                matrix[i][j] = rng.random() * 100
    return matrix


def test_large_open_tsp_uses_heuristic_and_is_complete():
    n_destinations = EXHAUSTIVE_LIMIT + 2
    matrix = _synthetic_matrix(n_destinations, seed=42)
    path = solve_tsp(matrix)
    assert len(path) == n_destinations + 1
    assert path[0] == 0
    assert sorted(path) == list(range(n_destinations + 1))
    assert solve_tsp(matrix) == solve_tsp(matrix)
