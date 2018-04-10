import random


def create_child(competitors_with_fitness):

    child = [None]*len(competitors_with_fitness(1, 2)) # Predefined size

    crossover_point = random.randint(3, len(competitors_with_fitness(1, 2)))  # XO point ranges from 4th element
    # to size of individual
    parent1 = competitors_with_fitness(1, 2)  # Best individual exists in 1st row, 2nd column (1st column holds fitness)
    parent2 = competitors_with_fitness(2, 2)  # Second best individual exists in 2nd row, 2nd column

    child[0:crossover_point] = parent1[0:crossover_point]
    child[crossover_point + 1:-1] = parent2[crossover_point + 1:-1]
    return child
