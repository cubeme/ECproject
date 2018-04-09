import random


def select_random_numbers(number_to_be_selected, pool_size):
    random_numbers = list()

    for i in range(number_to_be_selected):
        random_numbers.append(random.randint(0, pool_size - 1))

    return random_numbers
