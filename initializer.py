import random

from clash_checker import check_clash


def initialize_population(pop_size, sequence_length):
    population = list()

    for i in range(pop_size):
        # add new individual to population with key i
        population.append(create_individual(list(), sequence_length, [0, 1, 2]))

    return population


def create_individual(new_individual, sequence_length, possible_steps):
    # first step is always 1
    # and sequence of length n needs n-1 steps
    if len(new_individual) == sequence_length - 2:
        return new_individual

    # check if there are any steps left
    if not possible_steps:
        # new possible steps but remove step before last from possible steps (since it lead nowhere)
        possible_steps = [0, 1, 2]
        possible_steps.remove(new_individual[-1])
        # remove step before last (backtrack once more)
        del new_individual[-1]
        # try again with all step options
        return create_individual(new_individual, sequence_length, possible_steps)

    step = random.SystemRandom().choice(possible_steps)
    new_individual.append(step)

    if check_clash(new_individual):
        # and remove the step that led to the clash
        possible_steps.remove(step)
        # there was a clash, so remove the last step (backtrack)
        del new_individual[-1]
        return create_individual(new_individual, sequence_length, possible_steps)

    else:
        return create_individual(new_individual, sequence_length, [0, 1, 2])
