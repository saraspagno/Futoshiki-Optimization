import random
import numpy as np
import constants
from GeneticAlgo import GeneticAlgo


class GeneticAlgo2(GeneticAlgo):
    """
    this class represents a standard genetic algorithm
    """

    def create_random_grid(self):
        return super().create_random_grid()

    def fitness(self, grid):
        return super().fitness(grid)

    def optimize(self, grid):
        return super().optimize(grid)

    def initialize_population(self):
        super().initialize_population()

    def selection_with_prob(self):
        return super().selection_with_prob()

    def cross_over(self, grid1, grid2):
        return super().cross_over(grid1, grid2)

    def mutation(self, grid, prob):
        return super().mutation(grid, prob)

    def append_grid(self, new_population, new_fitness, grid):
        new_population.append(grid)
        new_fitness.append(self.fitness(grid))
        grid_optimized = self.optimize(grid)
        if self.fitness(grid_optimized) == 0:
            print(f'Solution found: {grid_optimized}')
            return True
        return False

    def start(self):
        """
        this method starts the Genetic Algorithm
        :param self: - self of class
        :return: none
        """
        self.initialize_population()
        iteration, restarts = 0, 0
        while restarts < constants.MAX_RESTARTS:
            if iteration == constants.MAX_ITERATIONS_EASY_6x6:
                print(f'\n\n\nRESTARTING FOR N.{restarts}')
                iteration = 0
                restarts += 1
                self.initialize_population()

            print(f'\n\n\nITERATION N.{iteration}')
            constants.print_population_and_fitness(self.population, self.pop_fitness)
            iteration += 1

            new_population = []
            new_fitness = []

            min_index = np.argmin(self.pop_fitness)
            min_fitness = self.pop_fitness[min_index]
            print('Min is: ', min_fitness)
            if min_fitness == 0:
                print(f'Solution found: {self.population[min_index]}')
                return restarts * constants.MAX_ITERATIONS_EASY_6x6 + iteration

            for i in range(constants.COPY_RATE):
                if self.append_grid(new_population, new_fitness, self.population[min_index].copy()):
                    return restarts * constants.MAX_ITERATIONS_EASY_6x6 + iteration
            for i in range(constants.SELECTION_RATE):
                grid1, grid2 = self.selection_with_prob()
                grid3 = self.cross_over(grid1, grid2)
                self.mutation(grid3, constants.MU)
                if self.append_grid(new_population, new_fitness, grid3):
                    return restarts * constants.MAX_ITERATIONS_EASY_6x6 + iteration
            indexes = random.sample(range(constants.M), constants.MUTATION_RATE)
            for i in indexes:
                self.mutation(new_population[i], 1)
                new_fitness[i] = self.fitness(new_population[i])
            self.population = np.array(new_population)
            self.pop_fitness = np.array(new_fitness)
        return -1
