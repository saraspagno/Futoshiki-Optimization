import constants

from Game import Game
from GeneticAlgo import GeneticAlgo


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
        constant_numbers.append(line_values)

    index += 1

    greater_constraints = []
    for i in range(int(lines[index])):
        index += 1
        line_values = list(map(int, lines[index].split(' ')))
        greater_constraints.append(line_values)

    # print(constant_numbers)
    # print(greater_constraints)

    return constant_numbers, greater_constraints


if __name__ == '__main__':
    constant_numbers, greater_constraints = parse_args('args.txt')
    game = Game(constant_numbers, greater_constraints)
    genetic_algo = GeneticAlgo(game)
