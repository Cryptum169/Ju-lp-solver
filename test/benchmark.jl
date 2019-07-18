using LPSolver
using BenchmarkTools

obj_func = [-3 -5];
constraint_arithmetic = [1 0;0 2;3 2];
constraint_boundary = [4 12 18];
simplex(obj_func, constraint_arithmetic, constraint_boundary) |> println

obj_func = [3 5 -6];
constraint_arithmetic = [-4 0 -10; 1 2 7; 0 -1 -1];
constraint_boundary = [-1 5 -1];
simplex(obj_func, constraint_arithmetic, constraint_boundary) |> println

obj_funcs = []
constraint_arithmetics = []
constraint_boundarys = []

println("------------------- a detailed profiling -----------------")

(@benchmark simplex(obj_func, constraint_arithmetic, constraint_boundary)) |> display
println()

println("------------------- do 10000 random trials after compilation (total time) -----------------")
while true
    size = rand(3:20)
    o = rand(-10:10, (1, size))
    ca = rand(-15:15, (size, size))
    cb = rand(-10:10, (1, size))
    try 
        simplex(o, ca, cb)
        push!(obj_funcs, o)
        push!(constraint_arithmetics, ca)
        push!(constraint_boundarys, cb)
    catch
        
    end

    length(obj_funcs) == 10000 && break
end

@time for i in 1:10000
    simplex(obj_funcs[i], constraint_arithmetics[i], constraint_boundarys[i])
end

