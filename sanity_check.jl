include("./src/LPSolver.jl")

using .LPSolver
using BenchmarkTools
obj_func = [3 5 -6];
constraint_arithmetic = [4 0 10; 1 2 7; 0 1 1];
constraint_boundary = [1 5 1];
sign = [-1 1 -1];

LPSolver.simplex(obj_func, constraint_arithmetic, constraint_boundary, sign);