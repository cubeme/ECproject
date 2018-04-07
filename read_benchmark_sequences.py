
def read_benchmark_file():
    benchmark_list = []
    with open("benchmark_sequences.txt") as data_file:
        for line in data_file:
            benchmark_list.append(list(line.strip('\n')))
        data_file.close()

    return benchmark_list
