import random
import in_plane
import kink_movement
import out_of_plane
import crank_shaft_rotation
from clash_checker import check_clash


def mutation_operator(individual, in_plane_prob, out_of_plane_prob, crank_prob, kink_prob, clashed_limit):
    random_number = random.random()
    mutated = list()
    clashed = 0

    while clashed_limit != clashed:  # applies mutation while there is still clash
        if random_number <= in_plane_prob:  # accumulated probabilities are if conditions: one if 4 is applied
            mutated = in_plane.in_plane_mutation(individual)
        elif in_plane_prob < random_number and random_number <= (in_plane_prob + out_of_plane_prob):
            mutated = out_of_plane.out_of_plane(individual)
        elif (out_of_plane_prob + out_of_plane_prob) < random_number and \
                random_number <= (in_plane_prob + out_of_plane_prob + crank_prob):
            mutated = crank_shaft_rotation.crank_shaft_rotation(individual)
        elif (in_plane_prob + out_of_plane_prob + crank_prob) < random_number and \
                random_number <= (in_plane_prob + out_of_plane_prob + crank_prob + kink_prob):
            mutated = kink_movement.kink_movement(individual)

        if check_clash(mutated) == True:  # if clashed, set mutated as original one, and undergo mutation again.

            mutated = individual
            clashed += 1
        else:  # if there was not any clash, break while loop and return mutated
            break
    return mutated
