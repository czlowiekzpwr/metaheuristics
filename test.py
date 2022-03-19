import tsp_solution
import tsprandom


prob = tsprandom.RandomTSProblem()
sol = tsp_solution.random_solution(20)
print(sol)
w = tsp_solution.k_random(sol, 5, prob)
print(w)

n = tsp_solution.nearliest_neightboor(sol, prob)
print(prob.getSolutionLength(n))

w = tsp_solution.k_random(sol, 5, prob)
print(w)