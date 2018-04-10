import random


def out_of_plane(individual):
    mutation_point = random.randint(0, len(individual) - 1)  # randomly choosing mutation point
    mutated = list()
    mutated[0:len(individual) - 1] = individual[0:-1]  # Coping individual ti manipulated copied one

    for i in range(mutation_point, len(individual) - 1):  # starting from mutation point, flip 1s to 0 Vs.
        if individual[i] == 0:
            mutated[i] = 1

        elif individual[i] == 1:
            mutated[i] = 0
            return mutated
