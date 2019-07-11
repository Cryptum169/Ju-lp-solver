module LPSolver

using LinearAlgebra

export simplex
@inbounds function simplex(objFunc::Array, A::Array, B::Array, sign::Array)
    num_obj_var = size(objFunc, 2)
    num_of_constraint = size(A, 2); # -> index from 1

    num_bigM = sum(sign .- 1) ÷ -2;
    big_M = num_bigM != 0;
    arg_where = nothing
    big_M_matrix = zeros(num_of_constraint, num_bigM);


    if big_M
        arg_where = findall(x -> x < 0, sign)
        big_M_value = maximum(abs.(B)) * 1000;
        big_M_vector = ones(num_bigM, 1) .* big_M_value;
        for (idx, value) in enumerate(arg_where)
            big_M_matrix[value[2], idx] = 1
        end
    end

    constraint_vec = zeros(1, num_of_constraint);
    objFunc = hcat(objFunc, constraint_vec, big_M_vector', 0);

    slack_var_matrix = Matrix{Float64}(I, num_of_constraint, num_of_constraint)
    for value in arg_where
        slack_var_matrix[value[2], value[2]] = -1;
    end

    tableau = vcat(objFunc, hcat(A, slack_var_matrix, big_M_matrix, B'));

    if big_M
        for value in arg_where
            tableau[1,:] -= big_M_value .* tableau[value[2] + 1, :]
        end
    end

    iter_limit = 10;
    counter = 0;

    while !all(tableau[1,:].>=0) && (counter < iter_limit)
        counter += 1
        min_idx = argmin(tableau[1, 1:end-1])
        result = Tuple{Float64, Int64}[]
        for (idx, items) in enumerate(tableau[2:end, min_idx])
            items == 0 && continue
            values = tableau[idx + 1, end] / items
            values < 0 && continue
            temp = (values, idx);
            push!(result, (temp));
        end

        sort!(result, by = x -> x[1]);
        normalizing_constrant = tableau[result[1][2] + 1, min_idx]
        tableau[result[1][2] + 1, :] /= abs(normalizing_constrant)
        for k = 1:num_of_constraint + 1
            if k == result[1][2] + 1
                continue
            end
            coefficient = tableau[k, min_idx]
            tableau[k, :] -= tableau[result[1][2] + 1, :] * coefficient
        end
    end

    result = Array{Float64}(undef,num_obj_var)
    for k = 1:num_obj_var
        if tableau[1, k] != 0
            result[k] = 0;
        else
            item_idx = findfirst(x -> x == 1, tableau[2:end, k]);
            result[k] = tableau[item_idx + 1, end];
        end
    end

    result
end

end
