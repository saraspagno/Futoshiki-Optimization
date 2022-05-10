import random
import numpy as np
import constants
from Game import Game


# def print_board(board):
#     print('\n'.join(['\t'.join([str(cell) for cell in j]) for j in board]))


class GeneticAlgo:
    def __init__(self, game: Game):
        self.game = game
        self.population = []
        self.initialize_population()
        print('Population:', self.population)

    def set_constants_in_grid(self, grid):
        for c in self.game.constant_numbers:
            grid[c[0], c[1]] = c[2]

    def create_random_grid(self):
        grid = np.array([[0 for i in range(constants.N)] for j in range(constants.N)])
        row_values = [i for i in range(5)]
        taken_indexes_by_row = [[], [], [], [], []]
        taken_values_by_row = [[], [], [], [], []]
        for c in self.game.constant_numbers:
            value = c[2]
            grid[c[0], c[1]] = value
            taken_indexes_by_row[c[0]].append(c[1])
            taken_values_by_row[c[0]].append(value)
        # for each row
        for i in range(constants.N):
            filled_indexes = taken_indexes_by_row[i]
            for value in range(1, constants.N + 1):
                if value not in taken_values_by_row[i]:
                    possible_indexes = [x for x in row_values if x not in filled_indexes]
                    random_index = random.choice(possible_indexes)
                    grid[i][random_index] = value
                    filled_indexes.append(random_index)
        return grid

    # function to create M random grids
    def initialize_population(self):
        for i in range(constants.M):
            self.population.append(self.create_random_grid())

    # function to receive a grid and return a score
    def fitness(self, grid):
        errors = 0
        # counting the greater constraint
        for i in range(len(self.game.constraints)):
            current = self.game.constraints[i]
            great = grid[current[0]][current[1]]
            small = grid[current[2]][current[3]]
            if great <= small:
                errors += constants.G

        # counting the columns constraint
        for column in grid.T:
            _, counts = np.unique(column, return_counts=True)
            # adding 0 if appears 1, 1 if appears 2, 2 if appears 3, etc.
            for occurrence in counts:
                errors += occurrence - 1

        return errors

    def selection(self):
        for i in range(constants.M):
            print('Fitness at:', i, 'is', self.fitness(self.population[i]))
