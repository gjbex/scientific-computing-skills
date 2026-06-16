#!/usr/bin/env python3
'''Simple repeated wall-clock benchmarking for CLI applications.'''

from __future__ import annotations

import argparse
import json
import math
import os
import shlex
import statistics
import subprocess
import sys
import time
from dataclasses import asdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class BenchmarkResult:
    '''Summary statistics for one benchmark configuration.'''

    command: list[str]
    threads: int | None
    runs: int
    warmup_runs: int
    return_code: int
    environment: dict[str, str]
    timings_seconds: list[float]
    mean_seconds: float
    median_seconds: float
    min_seconds: float
    max_seconds: float
    stddev_seconds: float


def parse_args() -> argparse.Namespace:
    '''Parse command-line arguments.'''

    parser = argparse.ArgumentParser(
        description='Repeated wall-clock timing for CLI applications.',
    )
    parser.add_argument(
        '--warmup',
        type=int,
        default=1,
        help='Number of warmup runs before measurements.',
    )
    parser.add_argument(
        '--runs',
        type=int,
        default=5,
        help='Number of measured runs.',
    )
    parser.add_argument(
        '--threads',
        default='',
        help='Comma-separated OMP_NUM_THREADS values to benchmark.',
    )
    parser.add_argument(
        '--env',
        action='append',
        default=[],
        metavar='NAME=VALUE',
        help='Extra environment variable assignment. Repeatable.',
    )
    parser.add_argument(
        '--json',
        type=Path,
        help='Optional path for JSON output.',
    )
    parser.add_argument(
        '--cwd',
        type=Path,
        help='Working directory for the benchmarked command.',
    )
    parser.add_argument(
        '--command',
        nargs=argparse.REMAINDER,
        required=True,
        help='Command to benchmark. Use --command ./app -- arg1 arg2.',
    )
    return parser.parse_args()


def parse_threads(raw_threads: str) -> list[int | None]:
    '''Convert a thread list specification into concrete values.'''

    if not raw_threads.strip():
        return [None]

    thread_values: list[int | None] = []
    for item in raw_threads.split(','):
        value = item.strip()
        if not value:
            continue
        thread_count = int(value)
        if thread_count < 1:
            msg = f'Invalid thread count: {thread_count}'
            raise ValueError(msg)
        thread_values.append(thread_count)

    if not thread_values:
        return [None]
    return thread_values


def parse_env(items: Iterable[str]) -> dict[str, str]:
    '''Parse repeated NAME=VALUE assignments into an environment mapping.'''

    environment: dict[str, str] = {}
    for item in items:
        if '=' not in item:
            msg = f'Invalid environment assignment: {item!r}'
            raise ValueError(msg)
        name, value = item.split('=', maxsplit=1)
        name = name.strip()
        if not name:
            msg = f'Invalid environment assignment: {item!r}'
            raise ValueError(msg)
        environment[name] = value
    return environment


def normalize_command(command: list[str]) -> list[str]:
    '''Remove the optional separator used after --command.'''

    if not command:
        raise ValueError('Missing command after --command.')
    if command[0] == '--':
        command = command[1:]
    if not command:
        raise ValueError('Missing executable after --command.')
    return command


def time_command(
    command: list[str],
    environment: dict[str, str],
    cwd: Path | None,
) -> tuple[int, float]:
    '''Execute a command once and return its status code and wall time.'''

    start_time = time.perf_counter()
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=environment,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    elapsed = time.perf_counter() - start_time
    return completed.returncode, elapsed


def build_result(
    command: list[str],
    threads: int | None,
    runs: int,
    warmup_runs: int,
    return_code: int,
    environment: dict[str, str],
    timings_seconds: list[float],
) -> BenchmarkResult:
    '''Create a benchmark summary from raw timings.'''

    stddev_seconds = 0.0
    if len(timings_seconds) > 1:
        stddev_seconds = statistics.stdev(timings_seconds)

    return BenchmarkResult(
        command=command,
        threads=threads,
        runs=runs,
        warmup_runs=warmup_runs,
        return_code=return_code,
        environment=environment,
        timings_seconds=timings_seconds,
        mean_seconds=statistics.mean(timings_seconds),
        median_seconds=statistics.median(timings_seconds),
        min_seconds=min(timings_seconds),
        max_seconds=max(timings_seconds),
        stddev_seconds=stddev_seconds,
    )


def run_benchmark(
    command: list[str],
    base_environment: dict[str, str],
    cwd: Path | None,
    threads: int | None,
    warmup_runs: int,
    runs: int,
) -> BenchmarkResult:
    '''Run warmups and measured timings for one thread setting.'''

    environment = os.environ.copy()
    environment.update(base_environment)
    if threads is not None:
        environment['OMP_NUM_THREADS'] = str(threads)

    return_code = 0
    for _ in range(warmup_runs):
        return_code, _ = time_command(command, environment, cwd)
        if return_code != 0:
            break

    timings_seconds: list[float] = []
    if return_code == 0:
        for _ in range(runs):
            return_code, elapsed = time_command(command, environment, cwd)
            if return_code != 0:
                break
            timings_seconds.append(elapsed)

    if return_code != 0:
        msg = (
            f'Command failed with return code {return_code}: '
            f'{shlex.join(command)}'
        )
        raise RuntimeError(msg)

    return build_result(
        command=command,
        threads=threads,
        runs=runs,
        warmup_runs=warmup_runs,
        return_code=return_code,
        environment=base_environment,
        timings_seconds=timings_seconds,
    )


def format_seconds(value: float) -> str:
    '''Format a timing value for tabular output.'''

    if math.isnan(value):
        return 'nan'
    return f'{value:.6f}'


def print_results(results: list[BenchmarkResult]) -> None:
    '''Print benchmark summaries as a compact table.'''

    headers = (
        'threads',
        'mean [s]',
        'median [s]',
        'stddev [s]',
        'min [s]',
        'max [s]',
    )
    rows: list[tuple[str, str, str, str, str, str]] = []
    for result in results:
        thread_label = 'default' if result.threads is None else str(result.threads)
        rows.append(
            (
                thread_label,
                format_seconds(result.mean_seconds),
                format_seconds(result.median_seconds),
                format_seconds(result.stddev_seconds),
                format_seconds(result.min_seconds),
                format_seconds(result.max_seconds),
            )
        )

    widths = [len(header) for header in headers]
    for row in rows:
        widths = [max(width, len(value)) for width, value in zip(widths, row)]

    header_line = '  '.join(
        header.ljust(width) for header, width in zip(headers, widths)
    )
    separator_line = '  '.join('-' * width for width in widths)
    print(header_line)
    print(separator_line)
    for row in rows:
        print('  '.join(value.ljust(width) for value, width in zip(row, widths)))


def main() -> int:
    '''Run the command-line benchmark driver.'''

    args = parse_args()

    if args.warmup < 0:
        raise ValueError('--warmup must be non-negative.')
    if args.runs < 1:
        raise ValueError('--runs must be at least 1.')

    command = normalize_command(args.command)
    thread_values = parse_threads(args.threads)
    environment = parse_env(args.env)

    results = [
        run_benchmark(
            command=command,
            base_environment=environment,
            cwd=args.cwd,
            threads=threads,
            warmup_runs=args.warmup,
            runs=args.runs,
        )
        for threads in thread_values
    ]

    print(f'command: {shlex.join(command)}')
    if environment:
        print(f'environment: {environment}')
    print_results(results)

    if args.json is not None:
        payload = [asdict(result) for result in results]
        args.json.write_text(json.dumps(payload, indent=2) + '\n')

    return 0


if __name__ == '__main__':
    sys.exit(main())
