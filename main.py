import argparse
import multiprocessing as mp

from crossover_operator import crossover
from fitness_evaluator import evaluate_fitness
from fitness_evaluator import get_best_individual
from initializer import initialize_population
from mutation_operator import mutate
from plotter import plot_individual
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

# set parameters
clash_limit = 20
m_sys_crossover = 20
crossover_rate = 0.8
in_plane_prob = 0.3
out_of_plane_prob = 0.3
crank_prob = 0.1
kink_prob = 0.3

# get hp sequence: [total minimum energy, sequence]
benchmark = read_benchmark_file()[args.benchmark_sequence]

print("sequence: " + " ".join(benchmark[1]))
print("length: {}, minimal energy: {}".format(len(benchmark[1]), benchmark[0]))

population = initialize_population(args.pop_size, len(benchmark[1]))

# list that contains best fitness at [0] and the corresponding individual at [1]
best = get_best_individual(population, benchmark[1])
best_fitness_value = best[0]
best_individual = best[1]

# pool for parallel execution with 4 processes
pool = mp.Pool(processes=4)

# do GA iterations
iterations = 0
while iterations < args.iterations and best_fitness_value > benchmark[0]:
    # get random tournament competitors
    random_tournament_indices = select_random_numbers(args.tournament_size, args.pop_size)

    competitors = list()
    for index in random_tournament_indices:
        competitors.append(population[index])

    # rank them according to fitness
    ranked_competitors = hold_tournament(competitors, benchmark[1])

    # take 2 best as parents
    parents = [ranked_competitors[0][1], ranked_competitors[1][1]]
    # get 2 worst individuals
    worst_two = [ranked_competitors[-1][1], ranked_competitors[-2][1]]

    # do crossover with parents
    # returns list with [child_fitness, child] as elements
    children = pool.apply(crossover, args=(parents, clash_limit, m_sys_crossover, crossover_rate, benchmark[1],))

    # replace individuals
    # right now there cannot be multiple copies of same individual in the tournament
    # if this changes, we have to pay attention when removing the competitors from the population
    for fitness_and_child, one_worst_ind in zip(children, worst_two):
        # get the index of the individual to be replaced
        del_index = population.index(one_worst_ind)
        # delete the individual
        del population[del_index]
        # insert the child at that index
        population.insert(del_index, fitness_and_child[1])
        # if that child has better fitness than the current best fitness, set new best individual
        if fitness_and_child[0] < best_fitness_value:
            best_fitness_value = fitness_and_child[0]
            best_individual = population[del_index]

    # get random individuals for mutation
    random_mutation_indices = select_random_numbers(args.mut_lambda, args.pop_size)

    individuals_to_mutate = list()

    # do not allow best individual to be mutated
    best_index = population.index(best_individual)
    if best_index in random_mutation_indices:
        # select new random number
        random_alt = select_random_numbers(1, args.pop_size)[0]
        while (random_alt == index) or (random_alt in random_mutation_indices):
            random_alt = select_random_numbers(1, args.pop_size)[0]

        index_of_best_index = random_mutation_indices.index(best_index)
        del random_mutation_indices[index_of_best_index]
        random_mutation_indices.insert(index_of_best_index, random_alt)

    for index in random_mutation_indices:
        individuals_to_mutate.append(population[index])

    # do mutation
    mutated_individuals = pool.apply(mutate, args=(individuals_to_mutate, in_plane_prob, out_of_plane_prob,
                                                   crank_prob, kink_prob, clash_limit,))

    # evaluate fitness of new mutants
    mutant_fitnesses = [pool.apply(evaluate_fitness, args=(mutant, benchmark[1],)) for mutant in mutated_individuals]

    # order in index list and mutated individual list should not have changed
    for index, fitness, mutant in zip(random_mutation_indices, mutant_fitnesses, mutated_individuals):
        if fitness < best_fitness_value:
            best_fitness_value = fitness
            best_individual = mutant

        # replace individuals
        del population[index]
        population.insert(index, mutant)

    iterations += 1

plot_individual(best_individual, benchmark[1])
print("Energy value: {}".format(best_fitness_value))

# todo: pioneer search, best-, average-, and worst-fitness every 10 generations, do measure and make diagrams, timing
