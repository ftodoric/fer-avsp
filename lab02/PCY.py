import numpy as np
import itertools as it
import time


def PCY(input_data):
    # load number of baskets
    N = input_data[0]

    # load the threshold
    s = input_data[1]   # 's' has value of 0 or 1
    threshold = s * N   # integer value (floor)

    # load number of compartments
    num_of_compartments = input_data[2]

    # load baskets
    baskets = input_data[3]

    # item counter
    item_c = {}

    # 1st PASS
    for basket in baskets:
        for item in basket:
            index = item - 1
            try:
                item_c[index] += 1
            except KeyError:
                item_c[index] = 1

    # calculate A - number of frequent pair candidates
    m = 0
    for count in item_c.values():
        if count >= threshold:
            m += 1
    A = int(m * (m - 1) / 2)

    # compartments for compression function
    compartments = [0 for i in range(num_of_compartments)]

    # 2nd PASS - compression
    item_c_len = len(item_c)
    for basket in baskets:
        for i, j in it.combinations(basket, 2):
            # condense item pair into a compartment
            # both items must be frequent
            if item_c[i - 1] >= threshold:
                if item_c[j - 1] >= threshold:
                    k = (i * item_c_len + j) % num_of_compartments
                    compartments[k] += 1

    # 3rd PASS - counting pairs
    # maps - key is pair (i, j), value is frequency
    pair_map = {}
    P = 0
    for basket in baskets:
        for pair in it.combinations(basket, 2):
            i, j = pair
            # both items must be frequent and in a frequent compartment
            if item_c[i - 1] >= threshold:
                if item_c[j - 1] >= threshold:
                    k = (i * item_c_len + j) % num_of_compartments
                    if compartments[k] >= threshold:
                        try:
                            pair_map[pair] += 1
                        except KeyError:
                            pair_map[pair] = 1
                            P += 1

    # sort the pair map descending by frequency
    X = dict(sorted(pair_map.items(),
             key=lambda item: item[1], reverse=True)).values()

    # return the result
    return (A, P, X)


if __name__ == '__main__':
    """ # start time
    start = time.time() """

    # get the data from an input file
    N = int(input())
    s = float(input())
    b = int(input())

    baskets = []
    for i in range(N):
        string_list = input().split(" ")
        itemset = [int(s) for s in string_list]
        baskets.append(itemset)

    # run PCY algorithm
    input_data = (N, s, b, baskets)
    A, P, X = PCY(input_data)

    # print the results
    print("{}\n{}".format(A, P))
    for count in X:
        print(count)

    """ # end time
    end = time.time()
    # print time elapsed
    print("Time elapsed: {}s".format(end - start)) """
