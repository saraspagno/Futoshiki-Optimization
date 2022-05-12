import constants

from Game import Game
from GeneticAlgo import GeneticAlgo


def parse_args(args_file):
    index = 0
    file = open(args_file)
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]

    constants.N = int(lines[0]) # the first line is the size of the matrix
    lines.remove(lines[0])
    constants.num_of_constants = int(lines[0]) # the second line is the number of given digits
    constant_numbers ={}
    for constant_value_place in lines[0:constants.num_of_constants]:
        line_values = list(map(int, constant_value_place.split(' ')))
        constant_numbers[line_values[0]]= {line_values[1]:line_values[2]}
        lines.remove(lines[0])
#  change code to check if the key already has a value, and add the new value and not replace it

    greater_constraints = []
    for i in range(int(lines[index])):
        index += 1
        line_values = [i - 1 for i in list(map(int, lines[index].split(' ')))]
        greater_constraints.append(line_values)

    print('Constant Numbers: ', constant_numbers)
    print('Greater Constraints: ', greater_constraints)

    return constant_numbers, greater_constraints


if __name__ == '__main__':
    constant_numbers, greater_constraints = parse_args('args.txt')
    game = Game(constant_numbers, greater_constraints)
    genetic_algo = GeneticAlgo(game)
    genetic_algo.selection()
