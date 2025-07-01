#!/usr/bin/env python3

import math

from common import read_input

CHALLENGES = 7


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def verify_output():
    for challenge_number in range(CHALLENGES):
        print(f'Challenge {challenge_number}')
        cities = read_input(f'input_{challenge_number}.csv')
        N = len(cities)
        for output_prefix in ('output', 'sample/random', 'sample/greedy', 'sample/sa'):
            output_file = f'{output_prefix}_{challenge_number}.csv'
            with open(output_file) as f:
                lines = f.readlines()
                assert lines[0].strip() == 'index'
                tour = [int(i.strip()) for i in lines[1:N + 1]]

            expected = set(range(N))
            actual = set(tour)

            if expected != actual:
                missing = expected - actual
                duplicated = [node for node in tour if tour.count(node) > 1]
                raise ValueError(
                    f"\n[Error] {output_file}\n"
                    f"  - Missing nodes: {missing if missing else 'None'}\n"
                    f"  - Duplicated nodes: {duplicated if duplicated else 'None'}"
                )

            # assert set(tour) == set(range(N))
            path_length = sum(distance(cities[tour[i]], cities[tour[(i + 1) % N]])
                              for i in range(N))
            print(f'{output_prefix:16}: {path_length:>10.2f}')
        print()


if __name__ == '__main__':
    verify_output()
