import random
import numpy as np
import constants
from Game import Game


# def print_board(board):
#     print('\n'.join(['\t'.join([str(cell) for cell in j]) for j in board]))

def print_population(population):
    print('Population:')
    for i in range(len(population)):
        print(f'{i}: {population[i]}')


def print_population_and_fitness(population, fitness):
    print('Population:')
    for i in range(len(population)):
        print(f'{i}: {population[i]}, fitness: {fitness[i]}')


class GeneticAlgo:
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
        row_values = [i for i in range(5)]
        taken_indexes_by_row = [[], [], [], [], []]
        taken_values_by_row = [[], [], [], [], []]
        for c in self.game.constant_numbers:
            value = c[2]
            grid[c[0], c[1]] = value
            taken_indexes_by_row[c[0]].append(c[1])
            taken_values_by_row[c[0]].append(value)
        # for each row
        for i in range(constants.N):
            filled_indexes = taken_indexes_by_row[i]
            for value in range(1, constants.N + 1):
                if value not in taken_values_by_row[i]:
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
                # errors += (occurrence - 1) * 2
                if occurrence != 1:
                    errors += pow(4, (occurrence - 1))
        return errors

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
        print_population_and_fitness(self.population, self.pop_fitness)
        print(
            f'Selection, chosen indexes: {chosen[0], chosen[1]}, with weights: {self.pop_fitness[chosen[0]], self.pop_fitness[chosen[1]]}')
        return self.population[chosen[0]], self.population[chosen[1]]

    def selection(self):
        print_population_and_fitness(self.population, self.pop_fitness)
        indexes = np.argpartition(self.pop_fitness, 2)
        print(
            f'Selection, chosen indexes: {indexes[0], indexes[1]}, with weights: {self.pop_fitness[indexes[0]], self.pop_fitness[indexes[1]]}')
        return self.population[indexes[0]], self.population[indexes[1]]

    # todo: how to implement different dividers? now it's always half
    def cross_over(self, grid1, grid2):
        new_grid = []
        for x in grid1[:len(grid1) // 2]:
            new_grid.append(x.tolist())
        for x in grid2[len(grid2) // 2:]:
            new_grid.append(x.tolist())
        return np.array(new_grid)

    def mutation(self, grid):
        do = random.random() < constants.M
        if do:
            random_row_index = random.choice(range(5))
            filled_indexes = []
            taken_values = []
            random_row = [0, 0, 0, 0, 0]
            for c in self.game.constant_numbers:
                value = c[2]
                row = c[0]
                column = c[1]
                if row == random_row_index:
                    random_row[column] = value
                    filled_indexes.append(column)
                    taken_values.append(value)
            for n in range(1, constants.N + 1):
                if n not in taken_values:
                    possible_indexes = [x for x in range(5) if x not in filled_indexes]
                    random_index = random.choice(possible_indexes)
                    random_row[random_index] = n
                    filled_indexes.append(random_index)
            grid[random_row_index] = random_row



    def replace(self, new_grid):
        new_fitness = self.fitness(new_grid)
        worst_index = np.argmax(self.pop_fitness)
        worst_grid = self.population[worst_index]
        if np.equal(new_grid, worst_grid).all():
            self.counter += 1
        else:
            self.counter = 0
        if self.counter == 5 or new_fitness == 0:
            return True
        self.population[worst_index] = new_grid
        self.pop_fitness[worst_index] = float(new_fitness)
        return False

    # def stop_algo(self):
    #     min_fitness = np.min(self.pop_fitness)
    #     print('Iteration min:', min_fitness)
    #     max_fitness = np.max(self.pop_fitness)
    #     print('Compare:', min_fitness, max_fitness)
    #     return min_fitness == 0

    def start(self):
        self.initialize_population()
        iteration = 0
        should_stop = False
        while not should_stop:
            print(f'\n\n\nITERATION N.{iteration}')
            print('Counter: ', self.counter)
            iteration += 1
            grid1, grid2 = self.selection_with_prob()
            grid3 = self.cross_over(grid1, grid2)
            self.mutation(grid3)
            should_stop = self.replace(grid3)
