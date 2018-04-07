import argparse

from initializer import initialize_population
from read_benchmark_sequences import read_benchmark_file

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
parser.add_argument('lambda', metavar='l', type=int, nargs='?', help='Mutation group size lambda.')
parser.add_argument('iterations', metavar='i', type=int, nargs='?',
                    help='The number of generations the algorithm will run.')
args = parser.parse_args()

benchmark_sequence = read_benchmark_file()[args.benchmark_sequence]

print(benchmark_sequence)

population = initialize_population(args.pop_size, len(benchmark_sequence))

for ind in population:
    print(ind)
