import numpy as np
import random

import constants


class Game:
    def __init__(self, constant_numbers, constraints):
        self.constraints = constraints
        self.constant_numbers = constant_numbers
        self.taken_indexes_by_row = [[] for i in range(constants.N)]
        self.taken_values_by_row = [[] for i in range(constants.N)]
        self.taken_columns_by_value = [[] for i in range(constants.N)]
        self.greater_by_row = [[] for i in range(constants.N)]
        self.smaller_by_row = [[] for i in range(constants.N)]

        self.pencil_init()

    def pencil_init(self):
        for c in self.constant_numbers:
            # if a constant value is 2
            if c[2] == 2:
                # check if a greater starts with its coordinates
                for g in self.constraints:
                    if g[0] == c[0] and g[1] == c[1]:
                        self.constant_numbers.append([g[2], g[3], 1])
                        self.constraints.remove(g)
            if c[2] == constants.N - 1:
                # check if a greater end with its coordinates
                for g in self.constraints:
                    if g[2] == c[0] and g[3] == c[1]:
                        self.constant_numbers.append([g[0], g[1], 5])
                        self.constraints.remove(g)

        for c in self.constant_numbers:
            self.taken_indexes_by_row[c[0]].append(c[1])
            self.taken_values_by_row[c[0]].append(c[2])
            self.taken_columns_by_value[c[2] - 1].append(c[1])

        for g in self.constraints:
            self.greater_by_row[g[0]].append(g[1])
            self.smaller_by_row[g[2]].append(g[3])

        row_values = [i for i in range(constants.N)]
        should_continue = True
        while should_continue:
            should_continue = False
            # for each row
            for i in range(constants.N):
                for value in [5, 1, 2, 3, 4]:
                    if value not in self.taken_values_by_row[i]:
                        if value == constants.N:
                            possible_indexes = [x for x in row_values if x not in (self.taken_indexes_by_row[i] + self.smaller_by_row[i] + self.taken_columns_by_value[value - 1])]
                        elif value == 1:
                            possible_indexes = [x for x in row_values if x not in (self.taken_indexes_by_row[i] + self.greater_by_row[i] + self.taken_columns_by_value[value - 1])]
                        else:
                            possible_indexes = [x for x in row_values if x not in (self.taken_indexes_by_row[i] + self.taken_columns_by_value[value - 1])]
                        if len(possible_indexes) == 1:
                            self.constant_numbers.append([i, possible_indexes[0], value])
                            self.taken_indexes_by_row[i].append(possible_indexes[0])
                            self.taken_values_by_row[i].append(value)
                            self.taken_columns_by_value[value - 1].append(possible_indexes[0])
                            should_continue = True
