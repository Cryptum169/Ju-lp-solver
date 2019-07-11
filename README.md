# Ju-lp-solver
Porting a LP solver written in Python to Julia. A Practice Project for learning Julia.

## Algorithm
Uses Simplex algorithm to solve a simple linearly constrained linear objective programming problem. Features Big-M method for initial infeasible solution. Python Code is the course homework for Georgia Tech CS {4,7}649 Robot Intelligent Planning. 

## Benchmark
Benchmark result is shown in the following. Benchmark on Julia is done by package BenchmarkTools and Python by package cProfile.

Python runs at 206.63 microsecond, averaged over 1000 function calls.
Julia runs at 47.63 microsecond, averaged over 10000 calls, provided by @benchmark.

```bash
$ julia benchmark.jl 
BenchmarkTools.Trial: 
  memory estimate:  33.91 KiB
  allocs estimate:  212
  --------------
  minimum time:     27.002 μs (0.00% GC)
  median time:      28.811 μs (0.00% GC)
  mean time:        37.164 μs (20.49% GC)
  maximum time:     41.594 ms (99.89% GC)
  --------------
  samples:          10000
  evals/sample:     1
$ python benchmark.py 
0.0002158868 second
```
