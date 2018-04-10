import random


def in_plane_mutation(individual):
    mutation_point = random.randint(0, len(individual) - 1)
    mutated = list()
    if individual[mutation_point] == 0:
        new_direction = random.choice(1, 2)
    elif individual[mutation_point] == 1:
        new_direction = random.choice(0, 2)
    else:
        new_direction = random.choice(0, 1)

    mutated[0: len(individual) - 1] = individual[0:-1]
    mutated[mutation_point] = new_direction
    return mutated
