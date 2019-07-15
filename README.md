# Ju-lp-solver
Porting a LP solver written in Python to Julia. A Practice Project for learning Julia.

## Algorithm
Uses Simplex algorithm to solve a simple linearly constrained linear objective programming problem. Features Big-M method for initial infeasible solution. Python Code is the course homework for Georgia Tech CS {4,7}649 Robot Intelligent Planning. 

## Unbounded Problem
Certain problems are unbounded, program throws exception when encountered with one. This is verified using scipy.optimize.linprog(), and is the reason try/catch exists in benchmark.* files 

## Benchmark
Benchmark result is shown in the following. Benchmark on Julia is done by package BenchmarkTools and Python by package cProfile.

Python runs at 1838 microsecond, averaged over 10000 function calls.
Julia runs at 36.095 microsecond, averaged over 10000 calls, provided by @benchmark.

```bash
$ julia benchmark.jl 
------------------- a detailed profiling -----------------
BenchmarkTools.Trial: 
  memory estimate:  33.00 KiB
  allocs estimate:  195
  --------------
  minimum time:     26.280 μs (0.00% GC)
  median time:      27.934 μs (0.00% GC)
  mean time:        36.095 μs (20.01% GC)
  maximum time:     43.205 ms (99.73% GC)
  --------------
  samples:          10000
  evals/sample:     1
------------------- do 10000 random trials after compilation (total time) -----------------
  1.125976 seconds (7.24 M allocations: 2.485 GiB, 14.10% gc time)
$ python benchmark.py 
0.0018386312295292997
```

## TODO
Run benchmark on scipy.optimize.linprog, since apparently my python code is nowhere near optimal, same goes for my Julia Code