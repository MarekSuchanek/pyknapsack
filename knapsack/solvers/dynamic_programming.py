import BitVector

from ..shared import KnapsackProblem, KnapsackSolution


def dynamic_programming(problem: KnapsackProblem, **params) -> KnapsackSolution:
    # Parameters
    print_msg = params.get('_print', print)
    max_capacity = problem.weight_limit
    n = problem.size
    print_msg('Dynamic Programming')

    # Create the table
    table = [[0 for _ in range(max_capacity + 1)] for _ in range(n + 1)]

    # Fill the table
    for item in range(1, n + 1):
        for capacity in range(1, max_capacity + 1):
            value, weight = problem[item - 1]

            # Calculate the maximum value with and without the item
            value_with_current = 0
            value_without_current = table[item - 1][capacity]

            # Check if the item fits in the knapsack
            if capacity >= weight:
                remaining_capacity = capacity - weight
                value_with_current = table[item - 1][remaining_capacity] + value

            # Select the maximum value
            table[item][capacity] = max(value_with_current, value_without_current)
            print_msg(f'[{item:02d}][{capacity:03d}] = {table[item][capacity]}')

    # Backtrack to find the selected items
    print_msg('Selected items:')
    items = []
    capacity = max_capacity
    for item in range(n, 0, -1):
        if table[item][capacity] != table[item - 1][capacity]:
            print_msg(f' - {item}')
            items.append(item - 1)
            capacity -= problem[item - 1][1]

    vector = BitVector.BitVector(bitlist=[1 if i in items else 0 for i in range(n)])
    return problem.evaluate(vector)
