import configparser
import json
import pathlib
import time

import click

from typing import Any

from .shared import KnapsackProblem
from .solvers import solve, SOLVERS


def load_problem_json(input_file: str) -> KnapsackProblem:
    filepath = pathlib.Path(input_file)
    if input_file.endswith('.json'):
        data = json.loads(filepath.read_text(encoding='utf-8'))
        problem = KnapsackProblem()
        problem.load_json(data)
        return problem

    raise ValueError(f'Unkown input file type: {input_file}')


def load_problem_line(input_line: str) -> KnapsackProblem:
    problem = KnapsackProblem()
    problem.load_line(input_line)
    return problem


def load_params(params_file: str, solver_name: str) -> dict[str, Any]:
    params = {}
    cp = configparser.ConfigParser()
    cp.read(params_file)
    if cp.has_section(solver_name):
        params = dict(cp[solver_name])
    return params


def print_msg(msg: str) -> None:
    click.echo(f'> {msg}')


def print_none(msg: str) -> None:
    pass


@click.command()
@click.argument('input_file', type=click.Path(exists=True, dir_okay=False))
@click.option('-s', '--solver-name', type=click.Choice(choices=list(SOLVERS.keys())))
@click.option('-t', '--measure-time', is_flag=True)
@click.option('-p', '--params-file', type=click.Path(exists=True, dir_okay=False), default='params.ini')
@click.option('-v', '--verbose', is_flag=True)
@click.option('-q', '--quiet', is_flag=True)
@click.option('-b', '--batch', is_flag=True)
@click.option('-o', '--output-file', type=click.Path(dir_okay=False))
def knapsack_cli(input_file: str, solver_name: str, measure_time: bool, params_file: str,
                 verbose: bool, quiet: bool, batch: bool, output_file: str):
    params = load_params(params_file, solver_name)
    params['_print'] = print_msg if verbose else print_none
    if batch:
        solve_batch(input_file, solver_name, measure_time, params, output_file, quiet)
    else:
        problem = load_problem_json(input_file)
        solve_one(problem, solver_name, measure_time, params, quiet)


def solve_one(problem: KnapsackProblem, solver_name: str, measure_time: bool, params: dict, quiet: bool):
    if not quiet:
        click.echo('Problem:')
        click.echo(f' - limit = {problem.weight_limit}')
        click.echo(f' - items({problem.size})')
        for i in range(problem.size):
            value, weight = problem[i]
            click.echo(f'   - (V={value}, W={weight})')
        click.echo('-' * 80)

    start = time.time()
    solution = solve(solver_name, problem, params)
    end = time.time()

    if measure_time:
        click.echo('-' * 80)
        click.echo(f'Time elapsed: {end - start} seconds')
    if not quiet:
        click.echo('-' * 80)
        click.echo('Solution:')
        click.echo(f' - value  = {solution.value}')
        click.echo(f' - weight = {solution.weight}')
        click.echo(f' - vector = {solution.vector}')
    else:
        click.echo(f'Solution: {solution.value} {solution.weight} {solution.vector}')
    return solution


def solve_batch(input_file: str, solver_name: str, measure_time: bool, params: dict,
                output_file: str | None, quiet: bool):
    input_str = pathlib.Path(input_file).read_text(encoding='utf-8')
    output_lines = []
    for input_line in input_str.splitlines():
        problem = load_problem_line(input_line)
        solution = solve_one(problem, solver_name, measure_time, params, quiet)
        result_line = problem.result_line(solution)
        click.echo('>> ' + result_line)
        output_lines.append(result_line)

    if output_file:
        pathlib.Path(output_file).write_text('\n'.join(output_lines), encoding='utf-8')
