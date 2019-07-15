import multiprocessing
from joblib import Parallel, delayed
from multiprocessing import Pool
import pstats
import numpy as np
from scipy.optimize import linprog
import sys
sys.path.append('..')
from src.simplexLP import simplex
import cProfile
import time
import io

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
print("Solver Solution")
print(simplex(c, A_ub, b_ub, sign))

A_ub_scipy = np.array([
    [-4, 0, -10],
    [1, 2, 7],
    [0, -1, -1]
])

b_ub_scipy = np.array([-1,5,-1])
print("Scipy.optimize.linprog solution")
print(linprog(c, A_ub_scipy, b_ub_scipy))

print("Detailed Profiling")
cProfile.run('simplex(c, A_ub, b_ub, sign)')

print("------------------- do 10000 random trials after compilation (total time) -----------------")

obj_func = []
ca = []
cb = []
s = []

for i in range(10000):
    size = np.random.randint(3,4,1)[0]
    obj_func_sin = np.random.randint(-10, 11, size)
    ca_sin = np.random.randint(0, 16, [size, size])
    cb_sin = np.random.randint(1, 11, size)
    s_sin = np.random.randint(0, 2, size) * 2 - 1

    try:
        simplex(obj_func_sin, ca_sin, cb_sin, s_sin)
        obj_func.append(obj_func_sin)
        ca.append(ca_sin)
        cb.append(cb_sin)
        s.append(s_sin)
    except:
        pass

    if len(obj_func) == 10000:
        break

print('10000 Solvable cases added')
    
start = time.time()
for i in range(len(obj_func)):
    simplex(obj_func[i], ca[i], cb[i], s[i])
end = time.time() - start
print(end / len(obj_func))

# inputs = range(10)

# def processInput(i):
#     return i * i

num_cores = multiprocessing.cpu_count()
print("{} cores active".format(num_cores))
start = time.time()
results = Parallel(n_jobs=num_cores)(delayed(simplex)(
    obj_func[i], ca[i], cb[i], s[i]) for i in range(len(obj_func)))
end = time.time() - start
print(end / len(obj_func))



# Commented Out cases for showing unbounded cases.
# c = np.array([8,7,-10])
# A = np.array([[6,14,9],
#  [8,7,14],
#  [0,5,7]])
# b = np.array([6,5,3])
# s = np.array([1,1,1])
# print(linprog(c,A,b))
# print(simplex(c, A, b, s))

# c = np.array([-3, -7, -9])
# A = np.array([[-9, -4, -13],
#               [-6, -11, -7],
#               [-6, -10, -4]])
# b = np.array([-8, -4, -2])
# # [-1 - 1 - 1]

# print(linprog(c, A, b))

# c = np.array([-2, -10, 2])
# A = np.array([[0, 2, 6],
#  [-13,0,-8],
#  [-11,-1,-3]])
# b = np.array([7,-1,-2])
# print(linprog(c, A, b))
