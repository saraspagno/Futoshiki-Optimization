import random
import numpy as np
import constants
from GeneticAlgo import GeneticAlgo


class GeneticAlgo3(GeneticAlgo):
    def append_grid(self, new_population, new_fitness, grid):
        """
        this appends a grid to the new population
        :param self: - self of class
        :param new_population - the new population list
        :param new_fitness - the new fitness list
        :param grid - the grid to append
        :return: none
        """
        grid_optimized = self.optimize(grid)
        if self.fitness(grid) <= self.fitness(grid_optimized):
            new_population.append(grid)
            new_fitness.append(self.fitness(grid))
        else:
            new_population.append(grid_optimized)
            new_fitness.append(self.fitness(grid_optimized))

    def start(self):
        """
        this method starts the Genetic Algorithm
        :param self: - self of class
        :return: none
        """
        self.initialize_population()
        iteration, restarts = 0, 0
        average, minimum = [], []
        while restarts < constants.MAX_RESTARTS:
            if iteration == constants.MAX_ITERATIONS:
                print(f'\n\n\nRESTARTING FOR N.{restarts}')
                iteration = 0
                restarts += 1
                self.initialize_population()

            print(f'\n\n\nITERATION N.{iteration}')
            constants.print_population_and_fitness(self.population, self.pop_fitness)
            average.append(self.get_average())
            minimum.append(self.get_minimum())
            iteration += 1

            new_population = []
            new_fitness = []

            min_index = np.argmin(self.pop_fitness)
            min_fitness = self.pop_fitness[min_index]
            print('Min is: ', min_fitness)
            if min_fitness == 0:
                print(f'Solution found: {self.population[min_index]}')
                return restarts * constants.MAX_ITERATIONS + iteration, average, minimum

            for i in range(constants.COPY_RATE):
                self.append_grid(new_population, new_fitness, self.population[min_index].copy())
            for i in range(constants.SELECTION_RATE):
                grid1, grid2 = self.selection_with_prob()
                grid3 = self.cross_over(grid1, grid2)
                self.mutation(grid3, constants.MU)
                self.append_grid(new_population, new_fitness, grid3)
            indexes = random.sample(range(constants.M), constants.MUTATION_RATE)
            for i in indexes:
                self.mutation(new_population[i], 1)
                new_fitness[i] = self.fitness(new_population[i])
            self.population = np.array(new_population)
            self.pop_fitness = np.array(new_fitness)
        return -1, average, minimum
