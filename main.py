import argparse

from initializer import initialize_population
from read_benchmark_sequences import read_benchmark_file
from selector import select_random_numbers
from tournament_holder import hold_tournament
from fitness_evaluator import get_best_individual

# there are three input arguments:
# benchmark sequence number: 0 = 20 amino acids, 1 = 24 amino acids, 2 = 25 amino acids, 3 = 36 amino acids,
# 4 = 48 amino acids, 5 = 50 amino acids, 6 = 60 amino acids, 7 = 64 amino acids,
# population size n,
# parent tournament selection size k,
# mutation group size lambda,
# and the maximum number of iterations i.
parser = argparse.ArgumentParser(description='GP Parameters.')
parser.add_argument('benchmark_sequence', metavar='b', type=int, nargs='?', help='Which benchmark sequence to use.')
parser.add_argument('pop_size', metavar='n', type=int, nargs='?', help='Population size.')
parser.add_argument('tournament_size', metavar='k', type=int, nargs='?', help='The tournament size k.')
parser.add_argument('mut_lambda', metavar='l', type=int, nargs='?', help='Mutation group size lambda.')
parser.add_argument('iterations', metavar='i', type=int, nargs='?',
                    help='The number of generations the algorithm will run.')
args = parser.parse_args()

benchmark_sequence = read_benchmark_file()[args.benchmark_sequence]

print(benchmark_sequence)

population = initialize_population(args.pop_size, len(benchmark_sequence))

# array that contains best fitness at [0] and the best individual at [1]
best_individual = get_best_individual(population, benchmark_sequence)

print("population")
for ind in population:
    print(ind)

print("best")
print(best_individual)

random_numbers_tournament = select_random_numbers(args.tournament_size, args.pop_size)

competitors = list()

for index in random_numbers_tournament:
    competitors.append(population[index])

ranked_competitors = hold_tournament(competitors, benchmark_sequence)

print("ranked")
for ind in ranked_competitors:
    print(ind)

parents = [ranked_competitors[0][1], ranked_competitors[1][1]]
worst_competitors = [ranked_competitors[-2][1], ranked_competitors[-1][1]]

print("parents")
print(parents)
print("worst two")
print(worst_competitors)

# do crossover with parents

# if one of children has better fitness than best individual, replace it

random_numbers_mutation = select_random_numbers(args.mut_lambda, args.pop_size)

individuals_to_mutate = list()

for index in random_numbers_mutation:
    individuals_to_mutate.append(population[index])

# do mutation

# do not allow best individual to be mutated
