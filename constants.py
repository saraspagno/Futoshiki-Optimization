N = 5  # size of grid
M = 100  # size of population

G = 2  # weight of an error for not respecting "greater" constraint
C = 2  # weight of an error for not respecting the "column" or "row" constraint

MU = 0.5  # mutation probability
STOP = 2  # after how many equal iterations to stop

MAX_ITERATIONS = 500
MAX_RESTARTS = 15
COPY_RATE = 0.1 * M
SELECTION_RATE = M - COPY_RATE
MUTATION_RATE = 0.2 * M


def print_population(population):
    print('Population:')
    for i in range(len(population)):
        print(f'{i}: {population[i]}')


def print_population_and_fitness(population, fitness):
    print('Population:')
    for i in range(len(population)):
        print(f'{i}:\n {population[i]}, fitness: {fitness[i]}')
