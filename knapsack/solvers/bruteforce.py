import BitVector

from ..shared import KnapsackProblem, KnapsackSolution


def bruteforce(problem: KnapsackProblem, **params) -> KnapsackSolution:
    # Parameters
    print_msg = params.get('_print', print)
    print_msg('Bruteforce')

    # Initial solution
    vector = BitVector.BitVector(size=problem.size)
    best = KnapsackSolution(
        vector=vector,
        weight=0,
        value=0,
        valid=True,
    )
    last = ~vector

    # Bruteforce loop
    iterations = 0
    for i in range(last.int_val() + 1):
        iterations += 1
        vec = BitVector.BitVector(intVal=i, size=problem.size)
        sol = problem.evaluate(vec)
        if sol.valid and sol.value > best.value:
            best = sol
        if sol.valid and sol.value == best.value and sol.weight < best.weight:
            best = sol
        print_msg(f'[{iterations:05d}] {vec} | V={sol.value} W={sol.weight} (best={best.value})')

    return best
