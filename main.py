import constants
import matplotlib.pyplot as plt
from Game import Game
from GeneticAlgo1 import GeneticAlgo1
from GeneticAlgo2 import GeneticAlgo2
from GeneticAlgo3 import GeneticAlgo3


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


def make_graph(algo_class, title):
    values, colors, labels = [], [], []
    for file in constants.inputs:
        print(file)
        constant_numbers, greater_constraints = parse_args(file)
        game = Game(constant_numbers, greater_constraints)
        genetic_algo = algo_class(game)
        values.append(genetic_algo.start())

    plt.figure(figsize=(10, 5))
    for i, val in enumerate(values):
        if val == -1:
            colors.append('silver')
            values[i] = (max(values))
            labels.append('No solution')
        else:
            colors.append('mediumseagreen')
            labels.append(str(val))
    plt.bar(constants.classes, values, color=colors, width=0.6)
    for i in range(len(values)):
        plt.text(i, values[i], labels[i], ha='center', bbox=dict(facecolor='whitesmoke', alpha=.5))
    plt.ylabel("Number of iterations until solution")
    plt.xlabel("Classes analyzed")
    plt.title(title)
    plt.show()


if __name__ == '__main__':
    make_graph(GeneticAlgo1, 'Genetic Algorithm Version 1')
    make_graph(GeneticAlgo2, 'Genetic Algorithm Version 2')
    make_graph(GeneticAlgo3, 'Genetic Algorithm Version 3')
    # constant_numbers, greater_constraints = parse_args('args_tests/easy/6x6/args1.txt')
    # game = Game(constant_numbers, greater_constraints)
    # genetic_algo = GeneticAlgo1(game)
    # genetic_algo.start()
