import constants

from Game import Game
from GeneticAlgo import GeneticAlgo
from GeneticAlgo2 import GeneticAlgo2
from GeneticAlgo3 import GeneticAlgo3
from Lamarck import Lamarck


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
    constant_numbers, greater_constraints = parse_args('args_tests/args4.txt')
    game = Game(constant_numbers, greater_constraints)
    genetic_algo = GeneticAlgo2(game)
    genetic_algo.start()

