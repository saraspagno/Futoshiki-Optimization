import numpy as np

import constants


class Game:
    def __init__(self, constant_numbers, constraints):
        self.constraints = constraints
        self.constant_numbers = constant_numbers
        # self.grid = np.array([[0 for i in range(constants.N)] for j in range(constants.N)])
        # self.set_constants()

    # def set_constants(self):
    #     for c in self.constant_numbers:
    #         self.grid[c[0], c[1]] = c[2]

    # def __str__(self):
    #     return '\n'.join(['\t'.join([str(cell) for cell in j]) for j in self.grid])
