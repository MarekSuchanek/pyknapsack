from ..shared import KnapsackProblem, KnapsackSolution

from .bruteforce import bruteforce
from .dynamic_programming import dynamic_programming
from .genetic_algorithm import genetic_algorithm
from .simulated_annealing import simulated_annealing
from .tabu_search import tabu_search


SOLVERS = {
    'annealing': simulated_annealing,
    'bruteforce': bruteforce,
    'dynamic': dynamic_programming,
    'genetic': genetic_algorithm,
    'tabu': tabu_search,
}


def solve(solver_name: str, problem: KnapsackProblem, params: dict) -> KnapsackSolution:
    if solver_name not in SOLVERS.keys():
        raise ValueError(f'Unknown solver {solver_name}')
    solver = SOLVERS.get(solver_name)
    return solver(problem, **params)
