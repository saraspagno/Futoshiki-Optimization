import numpy as np

import constants


class Game:
    def __init__(self, constant_numbers, constraints):
        self.constraints = constraints
        self.constant_numbers = constant_numbers
        self.taken_indexes_by_row = [[] for i in range(constants.N)]
        self.taken_values_by_row = [[] for i in range(constants.N)]
        for c in constant_numbers:
            self.taken_indexes_by_row[c[0]].append(c[1])
            self.taken_values_by_row[c[0]].append(c[2])


    # def set_constants(self):
    #     for c in self.constant_numbers:
    #         self.grid[c[0], c[1]] = c[2]

    # def __str__(self):
    #     return '\n'.join(['\t'.join([str(cell) for cell in j]) for j in self.grid])
