from clash_checker import check_clash
import create_child


# gets competitors, maximum clash and number of crossovers
def crossover(competitors_with_fitness, clash_limit, crossover_limit):
    children = list()
    for i in range(0, 2 * crossover_limit):  # we consider first child each time so for loop is repeated twice of that
        clashed = 0
        while clashed != clash_limit:  # while there is crash, continue making child

            children[i] = create_child.create_child(competitors_with_fitness)  # put created child in children set
            checker = check_clash(children[i])  # checks for clash

            if checker is True:  # if there was clash, adds one unit to clashed numbers
                clashed = +1
            else:
                break  # if there was not a clash, gets out of while loop

        if clash_limit == clashed:  # checks if while loop broke because we reached maximum clashed numbers
            children[i] = competitors_with_fitness(1, 2)  # if yes, then chooses first parent as child.
    return children
