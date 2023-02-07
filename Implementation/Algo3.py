from ortools.linear_solver import pywraplp
import time

total_time = 0
run_times = []
for i in range(50):
    start_time = time.time()
    def solve_assignment_problem(N, K, d, t):
        solver = pywraplp.Solver('solve_assignment_problem', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

        # Define variables
        x = {}
        y = {}
        for i in range(N + 1):
            for k in range(K):
                x[i, k] = solver.IntVar(0, 1, f"x_{i}_{k}")
        for i in range(N + 1):
            for j in range(N + 1):
                for k in range(K):
                    if i != j:
                        y[i, j, k] = solver.IntVar(0, 1, f"y_{i}_{j}_{k}")
        c = {}
        for k in range(K):
            c[k] = solver.IntVar(0, solver.infinity(), f"c_{k}")
        z = solver.IntVar(0, solver.infinity(),'z')

        # Constraints
        # Constraint: The relation of x, y, and c
        for k in range(K):
            solver.Add(c[k] == solver.Sum([d[i] * x[i, k] for i in range(N + 1)]) + solver.Sum([t[i][j] * y[i, j, k] for i in range(N + 1) for j in range(N + 1) if i != j]))
        for i in range(1, N + 1):
            solver.Add(solver.Sum([x[i, k] for k in range(K)]) == 1)


        solver.Add(solver.Sum([y[i, 0, k] for i in range(1, N + 1) for k in range(K) ]) == K)
        solver.Add(solver.Sum([y[0, j, k] for j in range(1, N + 1)  for k in range(K)]) == K)       

    #     for k in range(K):
    #         for i in range(1, N + 1):
    #             for j in range(1, N + 1):
    #                 if i != j:
    #                     solver.Add(y[i, j, k] <= x[i, k])
    #                     solver.Add(y[i, j, k] <= x[j, k])
    #                     solver.Add(y[i, j, k] >= x[i, k] + x[j, k] - 1)

        # Constraint: Flow assignment constraint
        # solver.Add(solver.Sum([y[i,j,k] for i in range(1,N+1) for j in range(1,N+1) for k in range(K) if i!= j]) == x[i,k] for i in range(1,N+1) for k in range(K))
        # solver.Add(solver.Sum([y[j,i,k] for i in range(1,N+1) for j in range(1,N+1) for k in range(K) if i!= j]) == x[i,k] for i in range(1,N+1) for k in range(K))
        for k in range(K):
            for i in range(1,N+1):
    #             if i!= j:
                # solver.Add(solver.Sum([y[i,j,k] for i in range(1,N+1) for k in range(K)]) == x[i,k])
                    solver.Add(solver.Sum([y[i,j,k] for j in range(1,N+1) if j != i]) == x[i,k])
            for i in range(1,N+1):
    #             if i != j:
                # solver.Add(solver.Sum([y[j,i,k] for i in range(1,N+1) for k in range(K)]) == x[i,k])
                    solver.Add(solver.Sum([y[j,i,k] for j in range(1,N+1) if j != i]) == x[i,k])

        for k in range(K):
            solver.Add(c[k] <= z)

        # Add DFJ sub-tour elimination constraints
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                if i != j:
                    s = solver.Sum([y[i, j, k] for k in range(K)])
                    solver.Add(s <= K - 1)

        solver.Minimize(z)
        

      # Solve and return the result
        if solver.Solve() == pywraplp.Solver.OPTIMAL:
            res = [c[k].solution_value() for k in range(K)], z.solution_value()
            print("Assignment costs for each team:", res[0])
            print("Minimum total cost:", res[1])
            paths = []
            for k in range(K):
                path = []
                for i in range(1, N + 1):
                    if x[i, k].solution_value() == 1:
                        path.append(i)
                    else:
                        continue
                paths.append(path)
            return paths
        else:
            return None
    # MAIN
    filename = r"C:\Users\Dell\OneDrive - Hanoi University of Science and Technology\Desktop\Data\Test data OpenERP\N_1000_K_100.txt"
    def INP(filename):
        with open(filename) as f:
            T = []
            for eachline in f:
                # line = map(int, eachline)
                T.append(eachline.split())
            N = int(T[0][0])
            K = int(T[0][1])
            d = [int(x) for x in T[1]]
            S = []
            for line in T[2:]:
                eachline = map(int, line)
                S.append(list(eachline))
            return N,K,d,S
    # N: số lượng khách hàng
    # K: số lượng nhân viên
    # M: thời gian bảo trì
    # S: thời gian di chuyển giữa 2 địa điểm
    N,K,d,t = INP(filename)
    d.insert(0,0)
    end_time = time.time()
    run_time = end_time - start_time
    run_times.append(run_time)
    print("Run time for iteration {}: {}".format(i, run_time))
    total_time += run_time
average_time = total_time / 50
print("Average run time: {}".format(average_time))
paths = solve_assignment_problem(N, K, d, t)
print(paths)
# Save result to a file
with open("run_times_N_1000_K_100.txt", "w") as file:
    file.write("Run times:\n")
    for i in range(50):
        file.write("Run" + str(i + 1) + ": " + str(run_times[i]) + "\n")
    file.write("Average run time:" + str(average_time) + "\n")
