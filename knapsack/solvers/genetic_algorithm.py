import random

import BitVector

from ..shared import KnapsackProblem, KnapsackSolution


def genetic_algorithm(problem: KnapsackProblem, **params) -> KnapsackSolution:
    # Parameters
    print_msg = params.get('_print', print)
    population_size = int(params.get('population_size', 10))
    generations = int(params.get('generations', 100))
    elite_size = int(params.get('elite_size', 0))
    mutation_rate = float(params.get('mutation_rate', 0.05))
    mutation_type = params.get('mutation_type', 'single')
    crossover_rate = float(params.get('crossover_rate', 0.8))
    crossover_type = params.get('crossover_type', 'one_point')
    selection_type = params.get('selection_type', 'tournament')
    # Prepare operators
    _mutate = _mutate_single
    if mutation_type == 'inverse':
        _mutate = _mutate_inverse
    elif mutation_type == 'swap':
        _mutate = _mutate_swap
    _crossover = _crossover_one_point
    if crossover_type == 'two_point':
        _crossover = _crossover_two_point
    elif crossover_type == 'uniform':
        _crossover = _crossover_uniform
    _selection = _selection_tournament
    if selection_type == 'roulette':
        _selection = _selection_roulette

    print_msg('Genetic Algorithm:')
    print_msg(f'  population_size={population_size}, generations={generations}, mutation_rate={mutation_rate},')
    print_msg(f'  crossover_rate={crossover_rate}, crossover_type={crossover_type}, selection_type={selection_type}')

    # Initial population
    population = _generate_population(problem, population_size)
    best = max(population, key=lambda x: x.value)
    print_msg(f'[00000] Initial best solution: {best.vector} | V={best.value} W={best.weight}')

    # Genetic algorithm loop
    for generation in range(generations):
        g = generation + 1
        new_population = []

        # Elitism (keep best solutions)
        if elite_size > 0:
            elite = sorted(population, key=lambda x: x.value, reverse=True)[:elite_size]
            new_population.extend(elite)

        # Generate new population
        for _ in range(population_size):
            # Selection
            parent1 = _selection(population, **params).vector
            parent2 = _selection(population, **params).vector
            # Crossover
            if random.uniform(0, 1) < crossover_rate:
                child_vector = _crossover(parent1, parent2)
            else:
                # Copy parent instead
                if random.uniform(0, 1) < 0.5:
                    child_vector = parent2
                else:
                    child_vector = parent1
            # Mutation
            if random.uniform(0, 1) < mutation_rate:
                child_vector = _mutate(child_vector)
            # Evaluate
            child = problem.evaluate(child_vector)
            if not child.valid:
                child = problem.repair(child)
            # Add to new population
            new_population.append(child)
        population = new_population
        best = max(population, key=lambda x: x.value)
        print_msg(f'[{g:05d}] Best solution: {best.vector} | V={best.value} W={best.weight}')

    return best


def _generate_population(problem: KnapsackProblem, population_size: int) -> list[KnapsackSolution]:
    population = []
    for _ in range(population_size):
        vector = BitVector.BitVector(size=problem.size)
        solution = problem.evaluate(vector)
        if not solution.valid:
            solution = problem.repair(solution)
        population.append(solution)
    return population


def _selection_tournament(population: list[KnapsackSolution], **params) -> KnapsackSolution:
    tournament_size = params.get('tournament_size', 3)
    tournament = random.sample(population, tournament_size)
    return max(tournament, key=lambda x: x.value)


def _selection_roulette(population: list[KnapsackSolution], **params) -> KnapsackSolution:
    total = sum(x.value for x in population)
    pick = random.uniform(0, total)
    current = 0
    for solution in population:
        current += solution.value
        if current > pick:
            return solution
    return population[-1]


def _crossover_one_point(parent1: BitVector.BitVector, parent2: BitVector.BitVector, **params) -> BitVector.BitVector:
    point = random.randint(1, parent1.length() - 1)
    child = BitVector.BitVector(size=parent1.length())
    for i in range(parent1.length()):
        if i < point:
            child[i] = parent1[i]
        else:
            child[i] = parent2[i]
    return child


def _crossover_two_point(parent1: BitVector.BitVector, parent2: BitVector.BitVector, **params) -> BitVector.BitVector:
    point_a = random.randint(1, parent1.length() - 1)
    point_b = random.randint(1, parent1.length() - 1)
    if point_a > point_b:
        point_a, point_b = point_b, point_a
    child = BitVector.BitVector(size=parent1.length())
    for i in range(parent1.length()):
        if point_a < i <= point_b:
            child[i] = parent2[i]
        else:
            child[i] = parent1[i]
    return child


def _crossover_uniform(parent1: BitVector.BitVector, parent2: BitVector.BitVector, **params) -> BitVector.BitVector:
    child = BitVector.BitVector(size=parent1.length())
    for i in range(parent1.length()):
        child[i] = parent1[i] if random.uniform(0, 1) < 0.5 else parent2[i]
    return child


def _mutate_inverse(vector: BitVector.BitVector) -> BitVector.BitVector:
    return ~vector


def _mutate_swap(vector: BitVector.BitVector) -> BitVector.BitVector:
    i = random.randint(0, vector.length() - 1)
    j = random.randint(0, vector.length() - 1)
    vector[i], vector[j] = vector[j], vector[i]
    return vector


def _mutate_single(vector: BitVector.BitVector) -> BitVector.BitVector:
    i = random.randint(0, vector.length() - 1)
    vector[i] = not vector[i]
    return vector
