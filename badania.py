import tsp_solution
import tsprandom
import time

def test_solution(problem, fun):
    start = time.time()

    solution = fun(problem)

    delta_time = time.time()-start
    return (delta_time, problem.getSolutionLength(solution))

def run():
    algs = [tsp_solution.k_random, tsp_solution.better_nearliest_neightboor,tsp_solution.opt2random_input, tsp_solution.cool_alg]
    with open("resluts2.csv", 'w') as file:
        for i in range (10,50):
            
            
            for j in range(10):
                file.write(f"{i};{j};")
                print(f"{i}, {j}")
                tprob = tsprandom.RandomTSProblem(i)
                for alg_idx  in range(len(algs)):
                    delta_time, fit = test_solution(tprob, algs[alg_idx])
                    file.write(f"{alg_idx};{delta_time};{fit};")

                file.write("\n")

if __name__ == '__main__':
    run()            


        
    

