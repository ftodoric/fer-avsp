import time


def load_data():
    # Load number of nodes & beta coef
    n, beta = input().split()
    n, beta = int(n), float(beta)

    # Load edge matrix
    matrix = []
    util_matrix = {}
    for i in range(n):
        matrix.append([int(element) for element in input().split()])
        for item in matrix[i]:
            try:
                util_matrix[item].append((i, len(matrix[i])))
            except KeyError:
                util_matrix[item] = [(i, len(matrix[i]))]

    # Load number of queries
    q = int(input())

    # Load queries
    queries = []
    for i in range(q):
        queries.append([int(element) for element in input().split()])

    return n, beta, matrix, util_matrix, q, queries


def node_rank(N, beta, edge_matrix, util_matrix, q, queries):
    # Initialize r
    r = [1/N for i in range(N)]
    r_next = [0 for i in range(N)]

    # Begin iterations
    to_print = [0 for i in range(q)]
    for i in range(max([row[1] for row in queries])):

        S = 0
        for j in range(N):
            sum = 0
            try:
                for item in util_matrix[j]:
                    sum += beta*r[item[0]]/item[1]
            except KeyError:
                pass

            r_next[j] = sum
            S += r_next[j]

        for j in range(N):
            r_next[j] += (1 - S)/N

        r = r_next[:]

        # Test whether some query asks for this amount of iterations
        for qu_index, qu in enumerate(queries):
            if qu[1] - 1 == i:
                to_print[qu_index] = r[qu[0]]

    for text in to_print:
        print("{:.10f}".format(text))

    return


if __name__ == "__main__":
    init_time = time.time()

    # Load graph data
    n, beta, edge_matrix, util_matrix, q, queries = load_data()

    # Compute query result using power iteration method
    node_rank(n, beta, edge_matrix, util_matrix, q, queries)

    finish_time = time.time()
    #print("Elapsed time: {}s".format(finish_time - init_time))
