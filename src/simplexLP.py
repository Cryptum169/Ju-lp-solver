import timeit
import re
import cProfile
import numpy as np
from scipy.optimize import linprog

np.set_printoptions(suppress=True,edgeitems=10)
np.core.arrayprint._line_width = 2000

def simplex(objFunc, mat_c, cons_A, sign):
    num_actual_var = objFunc.shape[0]

    # May be also check for constraint matching
    extra_variable = sign < 0
    num_of_big_M = np.sum(extra_variable)
    big_M = num_of_big_M != 0
    arg_where = None

    if big_M:
        # print("Big M Mode Initiated\n M" +
        #  "value set as 1000 times of largest absolute value"
        #  + "of the constraint")
        arg_where = np.argwhere(sign < 0)

    # Initialize tableau
    num_of_constraint = mat_c.shape[0]
    big_M_value = np.amax(np.absolute(cons_A)) * 1000
    big_M_vector = np.ones((num_of_big_M, 1)) * big_M_value

    big_M_matrix = np.zeros((num_of_constraint, num_of_big_M))

    if big_M:
        for idx, value in enumerate(arg_where):
            big_M_matrix[value[0]][idx] = 1

    objFunc = objFunc.reshape(1, objFunc.shape[0])

    constraint_vec = np.zeros((num_of_constraint,1)).reshape(1,
        num_of_constraint)
    big_M_vec = big_M_vector.reshape(1,num_of_big_M)
    objFunc = np.concatenate((objFunc, constraint_vec, big_M_vec, 
        np.zeros(1).reshape(1,1)), axis = 1)

    slack_variable_matrix = np.identity(num_of_constraint)
    for k in arg_where:
        slack_variable_matrix[k[0]][k[0]] = -1

    tableau = np.concatenate((mat_c, slack_variable_matrix, big_M_matrix,
    cons_A.T.reshape(num_of_constraint,1)), axis = 1)

    # Tableau Form Done
    tableau = np.concatenate((objFunc, tableau), axis = 0)

    if big_M:
        for value in arg_where:
            tableau[0][:] = tableau[0][:] - big_M_value * tableau[value + 1][:]

    iter_limit = 100
    counter = 0
    while not (tableau[0][:] >= 0).all() and counter < iter_limit:
        counter += 1
        minimize_idx = np.argmin(tableau[0][:-1])

        result = list()
        for idx, items in enumerate(tableau[1:,minimize_idx]):
            if items == 0:
                continue
            value = tableau[idx + 1, -1] / items
            if value < 0:
                continue

            result.append((value, idx))

        data = min(result, key = lambda t : t[0])
        normalizing_constant = tableau[data[1] + 1, minimize_idx]
        tableau[data[1] + 1, :] /= abs(normalizing_constant)

        for k in range(num_of_constraint + 1):
            if k == data[1] + 1:
                continue
            
            coefficient = tableau[k, minimize_idx]
            tableau[k, :] -= tableau[data[1] + 1, :] * coefficient
        
        # print(tableau)


    # print("Completed in {} iterations".format(counter))

    result = []
    for k in range(num_actual_var):
        if tableau[0][k] != 0:
            result.append(0)
        else:
            item_idx = np.where(tableau[1:][k] == 1)
            result.append(tableau[item_idx[0],-1][0])
    
    return result

# C as function for maximization
c = np.array([3,5,-6])

# A as constraint arithmetic
A_ub = np.array([
    [4,0,10],
    [1,2,7],
    [0,1,1]])

# B as constraint boundary
b_ub = np.array([1,5,1])

# Sign of constraints
sign = np.array([-1,1,-1])

import time
a = time.time()
for b in range(100):
    simplex(c, A_ub, b_ub, sign)
print(time.time() - a)

# cProfile.run('simplex(c, A_ub, b_ub, sign)')
