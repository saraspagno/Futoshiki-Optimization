N = 5  # size of grid
M = 100  # size of population

G = 2  # weight of an error for not respecting "greater" constraint

MU = 0.5  # mutation probability
STOP = 2  # after how many equal iterations to stop

MAX_ITERATIONS = 150
MAX_RESTARTS = 30
COPY_RATE = int(0.1 * M)
SELECTION_RATE = int(M - COPY_RATE)
MUTATION_RATE = int(0.2 * M)

inputs = ['args_tests/easy/5x5/args1.txt',
          'args_tests/easy/6x6/args2.txt',
          'args_tests/easy/7x7/args1.txt',
          'args_tests/tricky/5x5/args1.txt',
          'args_tests/tricky/6x6/args1.txt',
          'args_tests/tricky/7x7/args1.txt',
          ]

classes = ['Easy 5x5', 'Easy 6x6', 'Easy 7x7', 'Tricky 5x5', 'Tricky 6x6', 'Tricky 7x7']


def print_board(board):
    print('══' * int((N * 1.5 + 1)))
    for r, row in enumerate(board):
        print('║', end="")
        for v, value in enumerate(row):
            print(f' {value} ', end="")
        print('║\n', end="")
    print('══' * int((N * 1.5 + 1)))


def print_population_and_fitness(population, fitness):
    print('Population:')
    for i in range(len(population)):
        board = population[i]
        print(f'N.{i}, Fitness: {fitness[i]}:')
        print_board(board)