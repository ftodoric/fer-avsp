import numpy as np

a = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, "X", 9]])
for item in a[0]:
    print(item)
