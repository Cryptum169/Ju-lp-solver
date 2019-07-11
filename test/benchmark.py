import sys
sys.path.append('..')
from src.simplexLP import simplex
import cProfile
import time
import numpy as np
c = np.array([3, 5, -6])

# A as constraint arithmetic
A_ub = np.array([
    [4, 0, 10],
    [1, 2, 7],
    [0, 1, 1]])

# B as constraint boundary
b_ub = np.array([1, 5, 1])

# Sign of constraints
sign = np.array([-1, 1, -1])

a = time.time()
for i in range(1000):
    simplex(c, A_ub, b_ub, sign)
print("{0:.10f} second".format((time.time() - a) / 1000))
