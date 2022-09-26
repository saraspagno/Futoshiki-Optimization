import abc
from abc import ABC, abstractmethod
import random
import numpy as np
import constants
from Game import Game


class GeneticAlgo(ABC):
    """
    this class represents a standard genetic algorithm
    """

    def __init__(self, game: Game):
        """
        this method creates init the Genetic Algorithm
        :param game: from here we can deduct constant and greater values
        :return: none
        """
        self.game = game
        self.population = []
        self.pop_fitness = []

    def create_random_grid(self):
        """
        this method creates a random grid for the genetic algorithm.
        the random grid must rows respecting unique numbers 1 to N, and respecting constant elements of given board
        the element 1 won't appear as greater sign, and the element N won't appear as smaller sign
        :param self: self of class
        :return: the create grid
        """
        grid = np.array([[0 for i in range(constants.N)] for j in range(constants.N)])
        # for each row
        for i, row in enumerate(grid):
            row = random.choice(self.game.row_possibilities[i])
            grid[i] = row
        return grid

    # function to receive a grid and return a score (the highest fitness -> worst board)
    def fitness(self, grid):
        """
        this method evaluates the fitness of a given grid
        :param self: self of class
        :param grid: the grid to evaluate
        :return: fitness of grid
        """
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
            # adding 0 if appears 1, 2 if appears 2, 4 if appears 3, etc.
            for occurrence in counts:
                errors += (occurrence - 1)
                # if occurrence != 1:
                #     errors += pow(constants.C, (occurrence - 1))
        return float(errors)

    def initialize_population(self):
        """
        this method initializes a population for the genetic algorithm
        :param self: self of class
        :return: none
        """
        self.population = []
        self.pop_fitness = []
        for i in range(constants.M):
            self.population.append(self.create_random_grid())
            fitness_value = self.fitness(self.population[i])
            self.pop_fitness.append(float(fitness_value))

    def selection_with_prob(self):
        """
        this method select 2 grids from the population with probability on their fitness
        :param self: self of class
        :return: 2 grids from population
        """
        inverted = np.reciprocal(self.pop_fitness)
        normalized = np.divide(inverted, np.sum(inverted))
        chosen = np.random.choice(range(len(self.population)), 2, p=normalized)
        return self.population[chosen[0]], self.population[chosen[1]]

    def cross_over(self, grid1, grid2):
        """
        this method takes two grids and returns a third grid generated from cross-over
        :param self: self of class
        :param grid1: first grid for cross over
        :param grid2: second grid for cross over
        :return: the result of cross-over
        """
        divider = random.choice(range(5))
        new_grid = []
        for x in grid1[:divider]:
            new_grid.append(x.tolist())
        for x in grid2[divider:]:
            new_grid.append(x.tolist())
        return np.array(new_grid)

    def mutation(self, grid, prob):
        """
        this method takes a grid and performs a mutation with a certain probability
        :param self: self of class
        :param grid: grid to mutate
        :param prob: probability to whether performing the mutation or not
        :return: none
        """
        do = random.random() < prob
        if do:
            to_change = random.choice(range(1, constants.N + 1))
            random_row_indexes = random.sample(range(constants.N), to_change)
            for i in random_row_indexes:
                new_row = random.choice(self.game.row_possibilities[i])
                grid[i] = new_row
        return grid

    def optimize(self, grid):
        """
        this method locally optimizes one grid by replacing rows that have same values in columns
        :param self: self of class
        :param grid: the grid to optimize
        :return: the optimized grid
        """
        grid = grid.copy()
        for i in range(int(constants.N / 2)):
            for column in grid.T:
                a, counts = np.unique(column, return_counts=True)
                for i, occurrence in enumerate(counts):
                    if occurrence > 1:
                        indexes = np.where(a[i] == column)[0]
                        for j in indexes:
                            row = random.choice(self.game.row_possibilities[j])
                            grid[j] = row
                        break
            return grid

    def get_average(self):
        """
        this method returns the average fitness for an iteration
        :param self: - self of class
        :return: average
        """
        return sum(self.pop_fitness) / len(self.pop_fitness)

    def get_minimum(self):
        """
       this method returns the minimum fitness for an iteration
       :param self: - self of class
       :return: minimum
       """
        return min(self.pop_fitness)

    def start(self):
        """
        this method starts the Genetic Algorithm
        :param self: - self of class
        :return: none
        """
        pass
