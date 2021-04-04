import timeit

import_module = "import numpy as np"

test_code1 = """

l = [0 for i in range(int(1e8))]
counter = 0
for i in l:
    if i != 0:
        counter += 1

"""

test_code2 = """

l = np.zeros(int(1e8))
counter = np.count_nonzero(l)

"""

print(timeit.timeit(stmt=test_code1, number=1))
print(timeit.timeit(stmt=test_code2, number=1, setup=import_module))
