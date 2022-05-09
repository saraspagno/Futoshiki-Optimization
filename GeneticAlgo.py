import random
import numpy as np
import constants
from Game import Game


class GeneticAlgo:
    def __init__(self, game: Game):
        self.game = game
        self.population = []
        self.initialize_population()

    def set_constants_in_grid(self, grid):
        for c in self.game.constant_numbers:
            grid[c[0], c[1]] = c[2]

    def create_random_grid(self):
        grid = np.array([[0 for i in range(constants.N)] for j in range(constants.N)])
        row_values = [i for i in range(5)]
        taken_indexes_by_number = [[], [], [], [], []]
        taken_indexes_by_row = [[], [], [], [], []]
        taken_values_by_row = [[], [], [], [], []]
        for c in self.game.constant_numbers:
            value = c[2]
            grid[c[0], c[1]] = value
            taken_indexes_by_number[value - 1].append(c[1])
            taken_indexes_by_row[c[0]].append(c[1])
            taken_values_by_row[c[0]].append(value)
        print(taken_indexes_by_number)
        print(taken_indexes_by_row)
        print(taken_values_by_row)

        # for each row
        for i in range(constants.N):
            filled_indexes = taken_indexes_by_row[i]
            # for each value 1,...,N
            for value in range(1, constants.N + 1):
                if value not in taken_values_by_row[i]:
                    possible_indexes = [x for x in row_values if
                                        x not in filled_indexes and x not in taken_indexes_by_number[value - 1]]
                    random_index = random.choice(possible_indexes)
                    grid[i][random_index] = value
                    # updates
                    filled_indexes.append(random_index)
                    taken_indexes_by_number[value - 1].append(random_index)

        print(grid)

    # function to create M random grids
    def initialize_population(self):
        self.create_random_grid()
