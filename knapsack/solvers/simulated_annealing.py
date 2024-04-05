import math
import random

import BitVector

from ..shared import KnapsackProblem, KnapsackSolution


def simulated_annealing(problem: KnapsackProblem, **params) -> KnapsackSolution:
    # Parameters
    print_msg = params.get('_print', print)
    temperature_max = float(params.get('max_temperature', 100))
    temperature = temperature_max
    temperature_min = float(params.get('min_temperature', 0.01))
    cooling_rate = float(params.get('cooling_rate', 0.80))
    print_msg(f'Simulated Annealing: T={temperature_max} -> {temperature_min} CR={cooling_rate}')

    # Initial solution
    solution = _generate_initial_solution(problem)
    while solution is None:
        solution = _generate_initial_solution(problem)
    energy = solution.value
    best_solution = solution
    iteration = 0

    # Simulated Annealing loop
    while temperature > temperature_min:
        iteration += 1
        # print iteration aligned with leading zeros
        print_msg(f'[{iteration:05d}] {solution.vector} | V={solution.value} W={solution.weight} T={temperature:.2f}')
        # Generate a neighbor
        neighbor = _generate_neighbor(solution.vector)
        # Evaluate the neighbor
        neighbor_solution = problem.evaluate(neighbor)
        if not neighbor_solution.valid:
            neighbor_solution = problem.repair(neighbor_solution)
        neighbor_energy = neighbor_solution.value
        energy_delta = neighbor_energy - energy

        # Accept or reject the neighbor
        if _accept(energy_delta, temperature_max, iteration):
            solution = neighbor_solution
            energy = energy_delta

            # Update the best solution
            if solution.valid and solution.value > best_solution.value:
                best_solution = solution

        # Cool down
        temperature = temperature * cooling_rate

    return best_solution


def _accept(energy_delta: float, temperature: float, iteration: int) -> bool:
    if energy_delta > 0:
        # always accept better solutions
        return True
    else:
        # accept worse solutions with a probability
        r = random.uniform(0, 1)  # random number between 0 and 1
        return r < math.exp(-1 * energy_delta / temperature)


def _generate_initial_solution(problem: KnapsackProblem) -> KnapsackSolution:
    # Generate a random solution
    vector = BitVector.BitVector(size=problem.size)
    vector.gen_random_bits(width=problem.size)
    return problem.evaluate(vector)


def _generate_neighbor(vector: BitVector.BitVector) -> BitVector.BitVector:
    # Flip a random bit as a neighbor
    flip_index = random.randint(0, len(vector) - 1)
    neighbor = vector.deep_copy()
    neighbor[flip_index] = not neighbor[flip_index]
    return neighbor
