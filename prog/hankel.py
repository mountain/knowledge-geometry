import itertools
import numpy as np

def I(n):
    A = []
    for i in range(n):
        A.append([1 if j == i else 0 for j in range(n)])
    return A

Id = np.diag([1, 1, 1, 1, 1, 1])
M = np.diag([1, 1, 1, 1, 1, 1])
for m in itertools.permutations(I(6)):
    M = np.dot(M, Id + np.array([row for row in m], dtype=np.int))
print(M)