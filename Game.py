import numpy as np
import constants
import itertools


def print_possibilities(possibilities):
    for i in possibilities:
        line_list = i.tolist()
        print(line_list)
    print('\n')


def print_possibilities2(possibilities):
    for i in possibilities:
        print(i)
    print('\n')


class Game:
    """
    this class precedes the Genetic Algorithm and creates the parses the args into variables for the game.
    """

    def __init__(self, constant_numbers, constraints):
        """
        this method init the Game class
        :param self: self of class
        :param constant_numbers: the constant number given as args
        :param constraints: the greater/smaller constraints given as args
        """
        self.constraints = constraints
        self.constant_numbers = constant_numbers
        self.initial_possibilities = np.array(
            [[[True for i in range(constants.N)] for i in range(constants.N)] for i in range(constants.N)])
        self.row_possibilities = [[] for i in range(constants.N)]
        self.row_greater = [[] for i in range(constants.N)]

        for g in self.constraints:
            if g[0] == g[2]:
                self.row_greater[g[0]].append(g)

        self.pencil_init()
        print(self.constant_numbers)
        self.rows_init()
        print_possibilities2(self.row_possibilities)

    def rows_init(self):
        permutations = list(itertools.permutations([i for i in range(1, constants.N + 1)]))
        for i, row in enumerate(self.initial_possibilities):
            for perm in permutations:
                perm = list(perm)
                should_append = True
                for index, value in enumerate(perm):
                    index_list = row[index]
                    if not index_list[value - 1]:
                        should_append = False
                        break
                constraints = self.row_greater[i]
                for c in constraints:
                    if perm[c[1]] < perm[c[3]]:
                        should_append = False
                if should_append:
                    self.row_possibilities[i].append(perm)

    def pencil_init(self):
        """
        this method attempts to add as many constants as possible to the given
        there are some rules which allow us to 'pencil' mark the board and fill it to begin with
        :param self: self of class
        :return: none
        """
        # print_possibilities(self.initial_possibilities)
        self.apply_constants()
        self.apply_greater()
        is_done = False
        while not is_done:
            self.apply_constants()
            is_done = self.update_constants()

    def update_constants(self):
        """
        this method updates the constants in the game
        :param self: self of class
        :return: none
        """
        # print('Update constants')
        is_done = True
        # for each singular element in board:
        for i, row in enumerate(self.initial_possibilities):
            for j, element in enumerate(row):
                # if there is only one true
                if sum(element) == 1:
                    # get index of true
                    index = np.where(element == True)[0][0]
                    # check if not already in constants
                    if [i, j, index + 1] not in self.constant_numbers:
                        self.constant_numbers.append([i, j, index + 1])
                        is_done = False
        # for each row
        for i, row in enumerate(self.initial_possibilities):
            for j, element in enumerate(row.T):
                # if there is only one true
                if sum(element) == 1:
                    # get index of true
                    index = np.where(element == True)[0][0]
                    # check if not already in constants
                    if [i, index, j + 1] not in self.constant_numbers:
                        self.constant_numbers.append([i, index, j + 1])
                        is_done = False
        # for each column
        for i, column in enumerate(self.initial_possibilities.T):
            for j, element in enumerate(column):
                # if there is only one true
                if sum(element) == 1:
                    # get index of true
                    index = np.where(element == True)[0][0]
                    # check if not already in constants
                    if [index, j, i + 1] not in self.constant_numbers:
                        self.constant_numbers.append([index, j, i + 1])
                        is_done = False
        # print_possibilities(self.initial_possibilities)
        return is_done

    def apply_constants(self):
        """
        this method apply the constants constraints for the pencil mark
        :param self: self of class
        :return: none
        """
        # print('Constants')
        # 1. put all constant numbers
        for c in self.constant_numbers:
            index = c[2] - 1
            for row in self.initial_possibilities[c[0]]:
                row[index] = False
            for column in self.initial_possibilities[:, c[1]]:
                column[index] = False
            self.initial_possibilities[c[0], c[1], index] = True
            current = self.initial_possibilities[c[0], c[1]]
            for i in range(len(current)):
                if i != index:
                    current[i] = False
            for g in self.constraints:
                if g[0] == c[0] and g[1] == c[1]:
                    # go to smaller and remove all great or equal
                    smaller = self.initial_possibilities[g[2]][g[3]]
                    for i in range(len(smaller)):
                        if i > index:
                            smaller[i] = False
                if g[2] == c[0] and g[3] == c[1]:
                    # go to smaller and remove all great or equal
                    greater = self.initial_possibilities[g[0]][g[1]]
                    for i in range(len(greater)):
                        if i < index:
                            greater[i] = False
        # print_possibilities(self.initial_possibilities)

    def apply_greater(self):
        """
        this method apply the constants smaller/greater constraint for the pencil mark
        :param self: self of class
        :return: none
        """
        # print('Greater')
        for g in self.constraints:
            chain = [g]
            current = g
            chain_is_over = False
            while not chain_is_over:
                chain_is_over = True
                for c in self.constraints:
                    if current[2] == c[0] and current[3] == c[1]:
                        current = c
                        chain.append(current)
                        chain_is_over = False
                        break
            # to_change = constants.N - len(chain)
            for index, el in enumerate(chain):
                greater = self.initial_possibilities[el[0], el[1]]
                for i in range(len(chain) - index):
                    greater[i] = False
                smaller = self.initial_possibilities[el[2], el[3]]
                for i in range(constants.N - index - 1, constants.N):
                    smaller[i] = False

        # print_possibilities(self.initial_possibilities)
