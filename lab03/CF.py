from sys import argv

import numpy as np
from decimal import Decimal, ROUND_HALF_UP


# Cosine similarity
def cosine_sim(x, y):
    return np.sum(x*y) / np.sqrt(np.sum(x**2) * np.sum(y**2))


def collab_filter(user_item_table, item_loc, K, filter_type):
    # Adjust input arguments for different filtering methods
    if filter_type == 0:
        work_table = user_item_table.copy()
        target_row_index = item_loc[0]
        target_col_index = item_loc[1]
    elif filter_type == 1:
        work_table = user_item_table.copy().T
        target_row_index = item_loc[1]
        target_col_index = item_loc[0]

    # Get dimensions
    N = work_table.shape[0]
    M = work_table.shape[1]

    # Remember target column
    target_col = []
    for i in range(N):
        target_col.append(work_table[i, target_col_index])
    target_col = np.array(target_col)

    # Process all rows
    for i in range(N):
        # Calculate row mean
        mean = 0
        num_of_items = 0
        for item in work_table[i]:
            if item != -1:
                mean += int(item)
                num_of_items += 1
        mean /= num_of_items

        # Substract row mean from each row
        for j in range(M):
            if work_table[i, j] != -1:
                work_table[i, j] = work_table[i, j] - mean
            else:
                work_table[i, j] = 0.

    # Calculate cosine similarities of 1st row with other
    sims = {}
    for i in range(N):
        # If row is target row skip it
        if i == target_row_index:
            continue
        sim = cosine_sim(work_table[target_row_index],
                         work_table[i])
        sims[i] = sim

    # Pick K number of best similarities
    best_sims = {}
    sims = dict(sorted(sims.items(), key=lambda item: item[1], reverse=True))
    k = 0
    for row_index in sims:
        if sims[row_index] < 0.0:
            break
        if target_col[row_index] == -1:
            continue
        best_sims[row_index] = sims[row_index]
        k += 1
        if k == K:
            break

    # Aproximate rating
    numerator = 0.0
    denominator = 0.0
    for row_index in best_sims:
        numerator += best_sims[row_index] * float(target_col[row_index])
        denominator += best_sims[row_index]
    rating = numerator / denominator

    rating = Decimal(Decimal(rating).quantize(
        Decimal('.001'), rounding=ROUND_HALF_UP))

    return rating


# Get number of users and items
dimensions = input().split()
N = int(dimensions[0])
M = int(dimensions[1])

# Load user-item table
user_item_table = []
for i in range(N):
    user_item_table.append(input().replace("X", "-1").split())
user_item_table = np.array(user_item_table, dtype=np.double)

# Get number of queries
Q = int(input())

# Load queries
queries = []
for i in range(Q):
    queries.append([int(element) for element in input().split()])

# Process queries
for query in queries:
    # Parse query parameters
    row_index = query[0] - 1
    col_index = query[1] - 1
    filter_type = query[2]
    K = query[3]

    # Predict target rating
    rating_aproximation = collab_filter(user_item_table=user_item_table,
                                        item_loc=(row_index, col_index),
                                        filter_type=filter_type,
                                        K=K)

    print(rating_aproximation)
