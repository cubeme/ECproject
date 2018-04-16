import datetime

import matplotlib.pyplot as plt
from matplotlib import lines

from mapper import map_individual


def plot_individual(individual, hp_sequence):
    ind_coordinates = map_individual(individual)

    x_min = 0
    x_max = 0
    y_min = 0
    y_max = 0

    for coord in ind_coordinates:
        if coord.x > x_max:
            x_max = coord.x

        if coord.x < x_min:
            x_min = coord.x

        if coord.y > y_max:
            y_max = coord.y

        if coord.y < y_min:
            y_min = coord.y

    coord_min = x_min if x_min < y_min else y_min
    coord_max = x_max if x_max > y_max else y_max

    fig, ax = plt.subplots()
    plt.axis('scaled')
    ax.set_axis_off()
    ax.set_xlim(coord_min - 1, coord_max + 1)
    ax.set_ylim(coord_min - 1, coord_max + 1)

    # draw grid
    grid = [x + 0.5 for x in range(coord_min - 1, coord_max + 1)]

    for i in range(len(grid)):
        line = lines.Line2D([grid[i], grid[i]], [coord_min - 1, coord_max + 1], linewidth=1, color='black',
                            linestyle='dotted')
        ax.add_line(line)
        line = lines.Line2D([coord_min - 1, coord_max + 1], [grid[i], grid[i]], linewidth=1, color='black',
                            linestyle='dotted')
        ax.add_line(line)

    # draw circles
    for coord, point in zip(ind_coordinates, hp_sequence):
        if point == "H":
            circle = plt.Circle((coord.x, coord.y), 0.25, color='black', fill=False, clip_on=False)
        else:
            circle = plt.Circle((coord.x, coord.y), 0.25, color='black', clip_on=False)
        ax.add_artist(circle)

    # draw connections
    for i in range(len(ind_coordinates) - 1):
        y1 = ind_coordinates[i].y
        y2 = ind_coordinates[i + 1].y
        x1 = ind_coordinates[i].x
        x2 = ind_coordinates[i + 1].x
        # subtract/add circle radius to not draw inside circle
        if x1 == x2:
            y2 = y2 - 0.25 if y2 - y1 > 0 else y2 + 0.25
            y1 = y1 + 0.25 if y2 - y1 > 0 else y1 - 0.25

        if y1 == y2:
            x2 = x2 - 0.25 if x2 - x1 > 0 else x2 + 0.25
            x1 = x1 + 0.25 if x2 - x1 > 0 else x1 - 0.25

        line = lines.Line2D([x1, x2], [y1, y2], linewidth=1, color='black')
        ax.add_line(line)

    fig.savefig("plots/plot_best_individual_{}.png".format(datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S-%f')))
