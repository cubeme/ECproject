import matplotlib.pyplot as plt
from matplotlib import lines

from mapper import map_individual


def plot_individual(individual, hp_sequence):
    best_coordinates = map_individual(individual)

    x_max = 0
    x_min = 0

    y_max = 0
    y_min = 0

    for coord in best_coordinates:
        if coord.x > x_max:
            x_max = coord.x

        if coord.x < x_min:
            x_min = coord.x

        if coord.y > y_max:
            y_max = coord.y

        if coord.y < y_min:
            y_min = coord.y

    fig, ax = plt.subplots()
    plt.axis('scaled')
    ax.set_axis_off()
    ax.set_xlim(x_min - 1, x_max + 1)
    ax.set_ylim(y_min - 1, y_max + 1)

    for coord, point in zip(best_coordinates, hp_sequence):
        if point == "H":
            circle = plt.Circle((coord.x, coord.y), 0.25, color='black', fill=False, clip_on=False)
        else:
            circle = plt.Circle((coord.x, coord.y), 0.25, color='black', clip_on=False)
        ax.add_artist(circle)

    for i in range(len(best_coordinates) - 1):
        line = lines.Line2D([best_coordinates[i].x, best_coordinates[i + 1].x],
                            [best_coordinates[i].y, best_coordinates[i + 1].y],
                            linewidth=1, color='black')
        ax.add_line(line)

    fig.savefig("plot_best_individual.png")
