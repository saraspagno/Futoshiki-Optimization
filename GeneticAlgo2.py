import random
import numpy as np
import constants
from Game import Game


def print_population(population):
    print('Population:')
    for i in range(len(population)):
        print(f'{i}: {population[i]}')


def print_population_and_fitness(population, fitness):
    print('Population:')
    for i in range(len(population)):
        print(f'{i}: {population[i]}, fitness: {fitness[i]}')


class GeneticAlgo2:
    def __init__(self, game: Game):
        self.game = game
        self.population = []
        self.pop_fitness = []
        self.counter = 0
        # print_population(self.population)

    def set_constants_in_grid(self, grid):
        for c in self.game.constant_numbers:
            grid[c[0], c[1]] = c[2]

    def create_random_grid(self):
        grid = np.array([[0 for i in range(constants.N)] for j in range(constants.N)])
        row_values = [i for i in range(constants.N)]
        for c in self.game.constant_numbers:
            grid[c[0], c[1]] = c[2]
        # for each row
        for i in range(constants.N):
            filled_indexes = self.game.taken_indexes_by_row[i].copy()
            for value in range(1, constants.N + 1):
                if value not in self.game.taken_values_by_row[i]:
                    possible_indexes = [x for x in row_values if x not in filled_indexes]
                    random_index = random.choice(possible_indexes)
                    grid[i][random_index] = value
                    filled_indexes.append(random_index)
        return grid

    # function to receive a grid and return a score (highest fitness -> worst board)
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
            # adding 0 if appears 1, 2 if appears 2, 4 if appears 3, etc.
            for occurrence in counts:
                errors += (occurrence - 1)
                # if occurrence != 1:
                #     errors += pow(constants.C, (occurrence - 1))

        # counting the row constraint
        for row in grid:
            _, counts = np.unique(row, return_counts=True)
            # adding 0 if appears 1, 2 if appears 2, 4 if appears 3, etc.
            for occurrence in counts:
                errors += (occurrence - 1)
                # if occurrence != 1:
                #     errors += pow(constants.C, (occurrence - 1))

        # counting the constant constraint
        for c in self.game.constant_numbers:
            value = grid[c[0], c[1]]
            if value != c[2]:
                errors += constants.G

        return float(errors)

    # function to create M random grids
    def initialize_population(self):
        for i in range(constants.M):
            self.population.append(self.create_random_grid())
            fitness_value = self.fitness(self.population[i])
            self.pop_fitness.append(float(fitness_value))
        print_population_and_fitness(self.population, self.pop_fitness)

    def selection_with_prob(self):
        inverted = np.reciprocal(self.pop_fitness)
        normalized = np.divide(inverted, np.sum(inverted))
        chosen = np.random.choice(range(len(self.population)), 2, p=normalized)
        return self.population[chosen[0]], self.population[chosen[1]]

    def cross_over(self, grid1, grid2):
        # cross-over in rows
        if bool(random.getrandbits(1)):
            # divider = len(grid1) // 2
            # divider = 1
            divider = random.choice(range(5))
            new_grid = []
            for x in grid1[:divider]:
                new_grid.append(x.tolist())
            for x in grid2[divider:]:
                new_grid.append(x.tolist())
            return np.array(new_grid)
        # cross-over in columns
        else:
            grid1 = grid1.T
            grid2 = grid2.T
            divider = random.choice(range(5))
            new_grid = []
            for x in grid1[:divider]:
                new_grid.append(x.tolist())
            for x in grid2[divider:]:
                new_grid.append(x.tolist())
            return np.array(new_grid).T

    def mutation(self, grid, prob):
        do = random.random() < prob
        if do:
            to_change = int(0.3 * (constants.N * constants.N))
            i_indexes = []
            j_indexes = []
            for n in range(to_change):
                i_indexes.append(random.choice(range(constants.N)))
                j_indexes.append(random.choice(range(constants.N)))
            for n in range(to_change):
                random_value = random.choice(range(1, constants.N + 1))
                grid[i_indexes[n], j_indexes[n]] = random_value

    def optimize(self, grid):
        for g in self.game.constraints:
            if grid[g[0], g[1]] < grid[g[1], g[2]]:
                temp = grid[g[0], g[1]]
                grid[g[0], g[1]] = grid[g[1], g[2]]
                grid[g[1], g[2]] = temp

    def start(self):
        self.initialize_population()
        iteration = 0
        should_stop = False
        while not should_stop:
            print(f'\n\n\nITERATION N.{iteration}')
            iteration += 1
            print('Counter: ', self.counter)
            print_population_and_fitness(self.population, self.pop_fitness)

            new_population = []
            new_fitness = []

            min_index = np.argmin(self.pop_fitness)
            min_fitness = self.pop_fitness[min_index]
            print('Min is: ', min_fitness)
            if min_fitness == 0:
                break

            for i in range(int(0.1 * constants.M)):
                grid = self.population[min_index].copy()
                new_population.append(grid)
                new_fitness.append(self.fitness(grid))
            for i in range(int(0.9 * constants.M)):
                grid1, grid2 = self.selection_with_prob()
                grid3 = self.cross_over(grid1, grid2)
                self.mutation(grid3, 0.7)
                new_population.append(grid3)
                grid3_fitness = self.fitness(grid3)
                if grid3_fitness == 0:
                    print("Found")
                    break
                new_fitness.append(grid3_fitness)

            # for i in range(int(0.2 * constants.M)):
            #     copy = new_population[0].copy()
            #     self.mutation(copy, 1)
            #     self.optimize(copy)
            #     new_population.append(copy)
            #     new_fitness.append(self.fitness(copy))

            indexes = random.sample(range(constants.M), int(0.1 * constants.M))
            for i in indexes:
                self.mutation(new_population[i], 1)
                new_fitness[i] = self.fitness(new_population[i])

            self.population = np.array(new_population)
            self.pop_fitness = np.array(new_fitness)
