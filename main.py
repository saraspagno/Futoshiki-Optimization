import numpy as np

import constants

from Game import Game
from GeneticAlgo import GeneticAlgo
from GeneticAlgoTest3 import GeneticAlgoTest3


def parse_args(args_file):
    index = 0
    file = open(args_file)
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]

    constants.N = int(lines[index])
    index += 1

    constant_numbers = []
    for i in range(int(lines[index])):
        index += 1
        line_values = list(map(int, lines[index].split(' ')))
        line_values[0] -= 1
        line_values[1] -= 1
        constant_numbers.append(line_values)

    index += 1

    greater_constraints = []
    for i in range(int(lines[index])):
        index += 1
        line_values = [i - 1 for i in list(map(int, lines[index].split(' ')))]
        greater_constraints.append(line_values)

    print('Constant Numbers: ', constant_numbers)
    print('Greater Constraints: ', greater_constraints)
    return constant_numbers, greater_constraints


if __name__ == '__main__':
    constant_numbers, greater_constraints = parse_args('args_tests/easy/6x6/args1.txt')
    game = Game(constant_numbers, greater_constraints)
    genetic_algo = GeneticAlgoTest3(game)
    genetic_algo.start()
    # a = np.array([2, 2, 5, 5, 1])
    # a2, count = np.unique(a, return_counts=True)
    # print(a2)
    # print(count)
    # for i, oc in enumerate(count):
    #     if oc > 1:
    #         indexes = np.where(a2[i] == a)[0]
    #         print(f'Value is: {a2[i]}, indexes are: {indexes}')



