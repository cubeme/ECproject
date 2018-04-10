import random


def crank_shaft_rotation(individual):
    crank_shafts = set()
    mutated = list()
    mutated[0:len(individual) - 1] = individual[0:-1]  # Coping individual ti manipulated copied one

    for i in range(0, (len(individual) - 3)):
        # if there was a pattern like 0110 or 1001 keep index of first element
        if individual[i] == 0 and individual[i + 1] == 1 and individual[i + 2] == 1 and individual[i + 3] == 0:
            crank_shafts.add(i)  # add index to the set
        elif individual[i] == 1 and individual[i + 1] == 0 and individual[i + 2] == 0 and individual[i + 3] == 1:
            crank_shafts.add(i)
    crank_shaft_point = random.sample(crank_shafts, 1)  # randomly chooses one of indexes from set

    if individual[crank_shaft_point] == 0:  # converts 1001 to 0110 or Vs.
        mutated[crank_shaft_point] = 1
        mutated[crank_shaft_point + 1] = 0
        mutated[crank_shaft_point + 2] = 0
        mutated[crank_shaft_point + 3] = 1

    elif individual[crank_shaft_point] == 1:
        mutated[crank_shaft_point] = 0
        mutated[crank_shaft_point + 1] = 1
        mutated[crank_shaft_point + 2] = 1
        mutated[crank_shaft_point + 3] = 0

        return mutated
