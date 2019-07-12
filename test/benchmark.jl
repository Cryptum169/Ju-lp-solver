using LPSolver
using BenchmarkTools

obj_func = [3 5 -6];
constraint_arithmetic = [4 0 10; 1 2 7; 0 1 1];
constraint_boundary = [1 5 1];
sign = [-1 1 -1];

obj_funcs = []
constraint_arithmetics = []
constraint_boundarys = []
signs = []

println("------------------- a detailed profiling -----------------")

(@benchmark simplex(obj_func, constraint_arithmetic, constraint_boundary, sign)) |> display
println()

println("------------------- do 10000 random trials after compilation (total time) -----------------")

while true
    size = rand(3:20)
    o = rand(-10:10, (1, size))
    ca = rand(0:15, (size, size))
    cb = rand(1:10, (1, size))
    s = rand([-1, 1], (1,size))
    try 
        simplex(o, ca, cb, s)
        push!(obj_funcs, o)
        push!(constraint_arithmetics, ca)
        push!(constraint_boundarys, cb)
        push!(signs,s)
    catch
        
    end

    length(obj_funcs) == 10000 && break
end

@time for i in 1:10000
    simplex(obj_funcs[i], constraint_arithmetics[i], constraint_boundarys[i], signs[i])
end
