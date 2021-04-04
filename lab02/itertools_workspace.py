import itertools as it

l = [1, 2, 3, 4, 5]

for i, j in it.combinations(l, 2):
    print(i, j)
