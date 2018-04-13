import argparse

from crossover_operator import crossover
from fitness_evaluator import evaluate_fitness
from fitness_evaluator import get_best_individual
from initializer import initialize_population
from mutation_operator import mutate
from read_benchmark_sequences import read_benchmark_file
from selector import select_random_numbers
from tournament_holder import hold_tournament

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

clash_limit = 10
m_sys_crossover = 10
crossover_rate = 0.8
in_plane_prob = 0.4
out_of_plane_prob = 0.2
crank_prob = 0.1
kink_prob = 0.3

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
children = crossover(parents, clash_limit, m_sys_crossover, crossover_rate, benchmark_sequence)
# if one of children has better fitness than best individual, replace it
for fitness_and_child in children:
    if fitness_and_child[0] < best_individual[0]:
        best_individual[0] = fitness_and_child[0]
        best_individual[1] = fitness_and_child[1]

# replace individuals
# right now there cannot be multiple copies of same individual in the tournament
# if this changes, we have to pay attention when removing the competitors from the population
index = population.index(worst_competitors[0])
del population[index]
population.insert(index, children[0][1])

index = population.index(worst_competitors[1])
del population[index]
population.insert(index, children[1][1])

random_numbers_mutation = select_random_numbers(args.mut_lambda, args.pop_size)

individuals_to_mutate = list()

for index in random_numbers_mutation:

    # do not allow best individual to be mutated
    if population[index] == best_individual[1]:
        # select new random number
        random_alt = select_random_numbers(1, args.pop_size)[0]
        while random_alt == index:
            random_alt = select_random_numbers(1, args.pop_size)[0]
        individuals_to_mutate.append(population[random_alt])

    individuals_to_mutate.append(population[index])

# do mutation
mutated_individuals = mutate(individuals_to_mutate, in_plane_prob, out_of_plane_prob, crank_prob, kink_prob,
                             clash_limit)

for individual, mutant in zip(individuals_to_mutate, mutated_individuals):
    fitness = evaluate_fitness(mutant, benchmark_sequence)
    if fitness < best_individual[0]:
        best_individual[0] = fitness
        best_individual[1] = mutant

    # replace individuals
    index = population.index(individual)
    del population[index]
    population.insert(index, mutant)

print("new population")
for ind in population:
    print(ind)
