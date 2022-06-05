import constants
import matplotlib.pyplot as plt
import sys
import time

from Game import Game
from GeneticAlgo1 import GeneticAlgo1
from GeneticAlgo2 import GeneticAlgo2
from GeneticAlgo3 import GeneticAlgo3


def parse_args(args_file):
    """
    this function parses the file into arguments for algorithm
    :param args_file: - the file
    :return: none
    """
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


def make_common_graph(algo_class, title):
    """
    makes a common graph with each difficulty and board size for a specific algo class
    :param algo_class: - the algo class to use (standard, darwinian, lamarck)
    :param title - the title of the graph
    :return: none
    """
    values, colors, labels = [], [], []
    for file in constants.inputs:
        constant_numbers, greater_constraints = parse_args(file)
        game = Game(constant_numbers, greater_constraints)
        genetic_algo = algo_class(game)
        values.append(genetic_algo.start()[0])

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


def make_single_graph(algo_class, title, file):
    constant_numbers, greater_constraints = parse_args(file)
    game = Game(constant_numbers, greater_constraints)
    genetic_algo = algo_class(game)
    iterations, average, minimum = genetic_algo.start()
    indexes = [i for i in range(len(average))]
    plt.plot(indexes, average, color='r', label='average')
    plt.plot(indexes, minimum, color='b', label='minimum')
    plt.legend(loc="upper left")
    plt.xlabel("Iterations")
    plt.ylabel("Minimum and Average")
    plt.title(title)
    plt.show()


if __name__ == '__main__':
    # make_single_graph(GeneticAlgo1, "Standard Genetic Algorithm - Easy 7x7", 'args_tests/easy/7x7/args1.txt')
    # make_common_graph(GeneticAlgo1, 'Genetic Algorithm Version 1')
    # make_common_graph(GeneticAlgo2, 'Genetic Algorithm Version 2')
    # make_common_graph(GeneticAlgo3, 'Genetic Algorithm Version 3')

    print('Starting to run each algorithm version - Standard, Darwinian, Lamarck')
    time.sleep(2)

    # Standard Version
    print('Starting Standard version')
    time.sleep(2)
    constant_numbers, greater_constraints = parse_args(sys.argv[0])
    game = Game(constant_numbers, greater_constraints)
    genetic_algo = GeneticAlgo1(game)
    genetic_algo.start()
    time.sleep(10)

    # Darwinian Version
    print('Starting Darwinian version')
    time.sleep(2)
    constant_numbers, greater_constraints = parse_args(sys.argv[0])
    game = Game(constant_numbers, greater_constraints)
    genetic_algo = GeneticAlgo2(game)
    genetic_algo.start()
    time.sleep(10)

    # Lamarck Version
    print('Starting Lamarck version')
    time.sleep(2)
    constant_numbers, greater_constraints = parse_args(sys.argv[0])
    game = Game(constant_numbers, greater_constraints)
    genetic_algo = GeneticAlgo3(game)
    genetic_algo.start()
    time.sleep(10)
