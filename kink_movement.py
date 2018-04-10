import random


def kink_movement(individual):

    mutated = list()
    mutated[0:len(individual) - 1] = individual[0:-1]  # Copying individual ti manipulated copied one
    kink_index = set()   # a set to store indexes of (kink node - 1 )

    for i in range(0, len(individual)):  # finds the corresponding sequence and stores the index of (kind node - 1)

        if individual[i] == 1 and individual[i + 1] == 0 and individual[i + 2] == 1:  # 101
            kink_index.add(i)
        elif individual[i] == 2 and individual[i + 1] == 0 and individual[i + 2] == 1:  # 201
            kink_index.add(i)
        elif individual[i] == 1 and individual[i + 1] == 0 and individual[i + 2] == 2:  # 102
            kink_index.add(i)
        elif individual[i] == 2 and individual[i + 1] == 0 and individual[i + 2] == 2:  # 202
            kink_index.add(i)
        elif individual[i] == 2 and individual[i + 1] == 1 and individual[i + 2] == 2:  # 212
            kink_index.add(i)
        elif individual[i] == 0 and individual[i + 1] == 1 and individual[i + 2] == 2:  # 012
            kink_index.add(i)
        elif individual[i] == 2 and individual[i + 1] == 1 and individual[i + 2] == 0:  # 210
            kink_index.add(i)
        elif individual[i] == 0 and individual[i + 1] == 1 and individual[i + 2] == 0:  # 010
            kink_index.add(i)

    mutation_point = random.sample(kink_index, 1)  # randomly chooses one of indexes from set

    if individual[mutation_point] == 1 and individual[mutation_point + 1] == 0 \
            and individual[mutation_point + 2] == 1:     # 101 to 212
        mutated[mutation_point] = 2
        mutated[mutation_point+1] = 1
        mutated[mutation_point+2] = 2
    elif individual[mutation_point] == 2 and individual[mutation_point + 1] == 0 \
            and individual[mutation_point + 2] == 1:    # 201 to 012
        mutated[mutation_point] = 0
        mutated[mutation_point+1] = 1
        mutated[mutation_point+2] = 2
    elif individual[mutation_point] == 1 and individual[mutation_point + 1] == 0 \
            and individual[mutation_point + 2] == 2:    # 102 to 210
        mutated[mutation_point] = 2
        mutated[mutation_point+1] = 1
        mutated[mutation_point+2] = 0
    elif individual[mutation_point] == 2 and individual[mutation_point + 1] == 0 \
            and individual[mutation_point + 2] == 2:    # 202 to 010
        mutated[mutation_point] = 0
        mutated[mutation_point+1] = 1
        mutated[mutation_point+2] = 0
    elif individual[mutation_point] == 2 and individual[mutation_point + 1] == 1 \
            and individual[mutation_point + 2] == 2:    # 212 to 101
        mutated[mutation_point] = 1
        mutated[mutation_point+1] = 0
        mutated[mutation_point+2] = 1
    elif individual[mutation_point] == 0 and individual[mutation_point + 1] == 1 \
            and individual[mutation_point + 2] == 2:    # 012 to 201
        mutated[mutation_point] = 2
        mutated[mutation_point+1] = 0
        mutated[mutation_point+2] = 1
    elif individual[mutation_point] == 2 and individual[mutation_point + 1] == 1 \
            and individual[mutation_point + 2] == 0:    # 210 to 102
        mutated[mutation_point] = 1
        mutated[mutation_point+1] = 0
        mutated[mutation_point+2] = 2
    else:                                               # 010 to 202
        mutated[mutation_point] = 2
        mutated[mutation_point+1] = 0
        mutated[mutation_point + 2] = 2
        return mutated