from itertools import permutations

EXHAUSTIVE_LIMIT = 8


def _path_length(dist_matrix: list[list[float]], path: list[int]) -> float:
    total = 0.0
    for i in range(len(path) - 1):
        total += dist_matrix[path[i]][path[i + 1]]
    return total


def solve_exhaustive(dist_matrix: list[list[float]]) -> list[int]:
    n = len(dist_matrix)
    destinations = list(range(1, n))
    best_path: list[int] | None = None
    best_length = float("inf")
    for perm in permutations(destinations):
        path = [0, *perm]
        length = _path_length(dist_matrix, path)
        if length < best_length:
            best_length = length
            best_path = path
    return best_path


def nearest_neighbor(dist_matrix: list[list[float]]) -> list[int]:
    n = len(dist_matrix)
    unvisited = set(range(1, n))
    path = [0]
    current = 0
    while unvisited:
        nearest = min(unvisited, key=lambda node: dist_matrix[current][node])
        path.append(nearest)
        unvisited.remove(nearest)
        current = nearest
    return path


def two_opt(dist_matrix: list[list[float]], path: list[int]) -> list[int]:
    best = list(path)
    improved = True
    while improved:
        improved = False
        for i in range(1, len(best) - 1):
            for j in range(i + 1, len(best)):
                candidate = best[:i] + best[i : j + 1][::-1] + best[j + 1 :]
                if _path_length(dist_matrix, candidate) < _path_length(dist_matrix, best):
                    best = candidate
                    improved = True
    return best


def solve_tsp(dist_matrix: list[list[float]]) -> list[int]:
    n = len(dist_matrix) - 1
    if n <= EXHAUSTIVE_LIMIT:
        return solve_exhaustive(dist_matrix)
    return two_opt(dist_matrix, nearest_neighbor(dist_matrix))
