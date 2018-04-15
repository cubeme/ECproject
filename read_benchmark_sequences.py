import re


def read_benchmark_file():
    benchmark_list = []
    with open("benchmark_sequences.txt") as data_file:
        # skip first line with column headers
        next(data_file)
        for line in data_file:
            line_list = re.split('\s+', line.strip('\n'))
            # first item absolute minimum energy, second item hp sequence
            benchmark_list.append([int(line_list[0]), list(line_list[1])])
        data_file.close()

    return benchmark_list
