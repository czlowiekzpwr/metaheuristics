import numpy.random
import numpy as np
import tsproblem

#sequential & random
def random_solution(num_of_vortx):
    return np.random.permutation(num_of_vortx)+1

def sequential(num_of_vertex):
    return np.arange(1,num_of_vertex+1,1)

def k_random(problem, num_of_iter=100):
    best_solution = random_solution(len(problem.graph.nodes))
    best = problem.getSolutionLength(best_solution)
    for step in range(num_of_iter):
        new_candidate = random_solution(len(problem.graph.nodes))
        current = problem.getSolutionLength(new_candidate)
        if current < best:
            best = current
            best_solution = new_candidate
    return best_solution

def nearliest_neightboor(starting_point, problem):
    random_path=[starting_point]
    while len(random_path) < problem.size:
        best_partial_soution = None
        best_partial_solution_length =float('inf') 
        for next_node in range(1,problem.size+1):
            if next_node not in random_path:
                path_candidate = random_path.copy()
                path_candidate.append(next_node)
                candidate_length = problem.getPartialSolutionLength(path_candidate)
                if candidate_length < best_partial_solution_length:
                    best_partial_solution_length = candidate_length
                    best_partial_soution = path_candidate
            
        random_path = best_partial_soution
    return random_path
        
def better_nearliest_neightboor(problem):
    best_solution = None
    best_solution_length = float('inf')
    for i in range(1,problem.size+1):
        candidate = nearliest_neightboor(i, problem)
        candidate_length = problem.getSolutionLength(candidate)
        if candidate_length < best_solution_length:
            best_solution = candidate
            best_solution_length = candidate_length
    return best_solution

def opt2(input_solution, problem):
    best_solution = input_solution
    best_solution_lenght = problem.getSolutionLength(best_solution)
    is_solution_improving = True
    while is_solution_improving:
        curent_solution = best_solution
        curent_solution_length = best_solution_lenght
        for start in range(1,problem.size+1):
            for end in range(start+1,problem.size+1):
                local_solution = curent_solution.copy()

                local_solution[start:end+1]= np.flip(local_solution[start:end+1])
                local_solution_lenght = problem.getSolutionLength(local_solution)
                if local_solution_lenght < curent_solution_length:
                    curent_solution_length=local_solution_lenght
                    curent_solution = local_solution
        if curent_solution_length < best_solution_lenght:
            best_solution = curent_solution
            best_solution_lenght = curent_solution_length
        is_solution_improving = curent_solution_length < best_solution_lenght
    return best_solution

    
def opt2random_input(problem):
    solution = random_solution(len(problem.graph.nodes))
    return opt2(solution, problem)

def cool_alg(problem):
    return opt2(better_nearliest_neightboor(problem), problem)