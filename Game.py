import numpy as np
import constants


def print_possibilities(possibilities):
    for i in possibilities:
        line_list = i.tolist()
        print(line_list)
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
        self.taken_indexes_by_row = [[] for i in range(constants.N)]
        self.taken_values_by_row = [[] for i in range(constants.N)]
        self.greater_by_row = [[] for i in range(constants.N)]
        self.smaller_by_row = [[] for i in range(constants.N)]
        self.initial_possibilities = np.array([[[True for i in range(constants.N)] for i in range(constants.N)] for i in
                                               range(constants.N)])

        self.pencil_init()
        for c in self.constant_numbers:
            self.taken_indexes_by_row[c[0]].append(c[1])
            self.taken_values_by_row[c[0]].append(c[2])

        for g in self.constraints:
            self.greater_by_row[g[0]].append(g[1])
            self.smaller_by_row[g[2]].append(g[3])

    def pencil_init(self):
        """
        this method attempts to add as many constants as possible to the given
        there are some rules which allow us to 'pencil' mark the board and fill it to begin with
        :param self: self of class
        :return: none
        """
        print_possibilities(self.initial_possibilities)
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
        print('Update constants')
        is_done = True
        # for each element in each row:
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
        # for each element in each column:
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
        print_possibilities(self.initial_possibilities)
        return is_done

    def apply_constants(self):
        """
        this method apply the constants constraints for the pencil mark
        :param self: self of class
        :return: none
        """
        print('Constants')
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
                    print('inside smaller')
                    # go to smaller and remove all great or equal
                    smaller = self.initial_possibilities[g[2]][g[3]]
                    for i in range(len(smaller)):
                        if i > index:
                            smaller[i] = False
                if g[2] == c[0] and g[3] == c[1]:
                    print('inside greater')
                    # go to smaller and remove all great or equal
                    greater = self.initial_possibilities[g[0]][g[1]]
                    for i in range(len(greater)):
                        if i < index:
                            greater[i] = False
        print_possibilities(self.initial_possibilities)

    def apply_greater(self):
        """
        this method apply the constants smaller/greater constraint for the pencil mark
        :param self: self of class
        :return: none
        """
        print('Greater')
        for g in self.constraints:
            greater = self.initial_possibilities[g[0], g[1]]
            greater[0] = False
            smaller = self.initial_possibilities[g[2], g[3]]
            smaller[-1] = False
        print_possibilities(self.initial_possibilities)
