import random

import BitVector

from ..shared import KnapsackProblem, KnapsackSolution


def tabu_search(problem: KnapsackProblem, **params) -> KnapsackSolution:
    # Parameters
    print_msg = params.get('_print', print)
    max_iterations = int(params.get('max_iterations', 20))
    tabu_size = int(params.get('tabu_size', 10))  # static tabu size
    neighborhood_size = int(params.get('neighborhood_size', 1))  # number of neighbors to evaluate
    tabu_list = []
    print_msg(f'Tabu Search: {max_iterations} iterations, tabu_size={tabu_size}, neighborhood_size={neighborhood_size}')

    # Initial solution
    solution = _generate_initial_solution(problem)
    best_solution = solution
    best_value = solution.value
    tabu_list.append(solution)

    # Tabu Search loop
    for i in range(max_iterations):
        iteration = i + 1
        print_msg(f'[{iteration:05d}] {solution.vector} | V={solution.value} W={solution.weight} (best={best_value})')
        # Generate a neighborhood
        neighborhood = _generate_neighborhood(solution, neighborhood_size, problem, tabu_list, iteration, max_iterations)
        # Generate a neighbor
        neighbor_solution = _get_best_neighbor(neighborhood)
        neighbor_value = neighbor_solution.value

        # Update the best solution
        if neighbor_value > best_value:
            best_solution = neighbor_solution
            best_value = neighbor_value

        # Update the current solution
        solution = neighbor_solution

        # Update the tabu list
        tabu_list.append(solution)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

    return best_solution


def _generate_initial_solution(problem: KnapsackProblem) -> KnapsackSolution:
    # Generate a random solution
    vector = BitVector.BitVector(size=problem.size)
    vector.gen_random_bits(width=problem.size)
    return problem.evaluate(vector)


def _generate_neighborhood(solution: KnapsackSolution, neighborhood_size: int, problem: KnapsackProblem,
                           tabu_list: list[KnapsackSolution], iteration: int,
                           max_iterations: int) -> list[KnapsackSolution]:
    # Generate a random sample of solutions
    neighborhood = []
    while len(neighborhood) < neighborhood_size:
        neighbor = _generate_neighbor_vector(solution.vector)
        neighbor_solution = problem.evaluate(neighbor)
        if not neighbor_solution.valid:
            neighbor_solution = problem.repair(neighbor_solution)
        if (neighbor_solution not in tabu_list or
                _aspiration(neighbor_solution, solution, iteration, max_iterations)):
            neighborhood.append(neighbor_solution)
    return neighborhood


def _aspiration(neighbor: KnapsackSolution, solution: KnapsackSolution,
                iteration: int, max_iterations: int) -> bool:
    # Aspiration criteria
    #  overcome tabu if the neighbor is better than the current solution
    #  and we are in the first half of the iterations
    return neighbor.value > solution.value and iteration < max_iterations / 2


def _get_best_neighbor(sample: list[KnapsackSolution]) -> KnapsackSolution:
    # Find the best solution in the sample
    best = sample[0]
    for sol in sample:
        if sol.value > best.value:
            best = sol
    return best


def _generate_neighbor_vector(vector: BitVector.BitVector) -> BitVector.BitVector:
    # Flip a random bit as a neighbor
    flip_index = random.randint(0, len(vector) - 1)
    neighbor = vector.deep_copy()
    neighbor[flip_index] = not neighbor[flip_index]
    return neighbor
