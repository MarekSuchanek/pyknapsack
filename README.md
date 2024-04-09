# PyKnapsack - 0/1 Knapsack Problem Solver in Python

*Simple Python implementation of the 0/1 Knapsack Problem Solver in different ways.*

## Usage

You can simply install and run the CLI:

```
python -m venv venv
source venv/bin/activate
pip install .

knapsack --help
knapsack data/test001.json -s genetic -t -v
```

There are various solvers available (see below). You can also provide additional parameters via `params.ini` file ([example](params.ini) is part of the project).

Input is expected in the following JSON format:

```json
{
  "weight_limit": 5,
  "items": [
    {
      "value": 2,
      "weight": 4
    },
    {
      "value": 4,
      "weight": 3
    },
    {
      "value": 1,
      "weight": 2
    }
  ]
}
```

### Batch mode

You can also run the solver in batch mode (`-b`, `--batch`), in that case it expects the file with problem instance in a row:

```txt
ID n M [B] w1 v1 w2 v2 ... wn vn
```

where:
- `ID` - unique identifier of the problem instance
- `n` - number of items
- `M` - weight limit
- `B` - value limit (optional, expected in case of negative `ID`)
- `w1`, `w2`, ..., `wn` - weights of items
- `v1`, `v2`, ..., `vn` - values of items

You can specify output file (`-o`, `--output`) to save the results in format:

```txt
ID value i1 i2 ... in
```

where:
- `ID` - unique identifier of the problem instance
- `value` - value of the best solution
- `i1`, `i2`, ..., `in` - 0/1 whether the item is in the knapsack or not

## Solvers

Solvers are selected using `--solver` option. Each solver may have its own parameters that can be set in `params.ini` file.

### Brute Force (`bruteforce`)

It is the simplest way to solve the problem. It generates all possible combinations of items and selects the one with the highest value.

### Dynamic Programming (`dynamic`)

It is a more efficient way to solve the problem. It uses a table to store the best value for each weight and item.

### Genetic Algorithm (`genetic`)

It is a heuristic way to solve the problem. It uses a [genetic algorithm](https://en.wikipedia.org/wiki/Genetic_algorithm) to find the best solution.

There are several parameters that can be set in `params.ini` file:

- `population_size` - number of individuals in the population
- `generations` - number of generations
- `elite_size` - number of the best individuals to keep in the next generation automatically (elitism)
- `mutation_rate` - probability of mutation
- `mutation_type` - mutation method (`single`, `inverse`, `swap`)
- `crossover_rate` - probability of crossover
- `crossover_type` - crossover method (`one_point`, `two_point`, `uniform`)
- `selection_type` - selection method (`roulette`, `tournament`)

### Simulated Annealing (`annealing`)

It is a heuristic way to solve the problem. It uses a [simulated annealing algorithm](https://en.wikipedia.org/wiki/Simulated_annealing) to find the best solution.

There are several parameters that can be set in `params.ini` file:

- `max_temperature` - initial temperature
- `min_temperature` - final temperature
- `cooling_rate` - cooling rate (temperature decrease)

### Tabu Search (`tabu`)

It is a heuristic way to solve the problem. It uses a [tabu search algorithm](https://en.wikipedia.org/wiki/Tabu_search) to find the best solution.

There are several parameters that can be set in `params.ini` file:

- `max_iterations` - number of iterations
- `tabu_size` - number of items in the tabu list
- `neighborhood_size` - number of neighbors to consider

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
