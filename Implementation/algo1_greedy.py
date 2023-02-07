import math
import numpy as np
import statistics
import time

iters = 100
results = []
times = []
def INP(filename):
    with open(filename) as f:
        T = []
        for eachline in f:
            # line = map(int, eachline)
            T.append(eachline.split())
        N = int(T[0][0])
        K = int(T[0][1])
        M = [int(x) for x in T[1]]
        S = []
        for line in T[2:]:
            eachline = map(int, line)
            S.append(list(eachline))
        return N,K,M,S


def TSP_tour_cost(y,c,d,N):
    y.append(y[0])
    cost = 0
    for i in range(N):
        cost += (c[y[i]][y[i+1]] + d[y[i]])
    y.pop(-1)
    return cost

# print(TSP_tour_cost(y,c,N))
# TSP_tour_plot(y,location,N)

def TSP_onestep_opt2(y,c,N):
    y.append(y[0])
    for i in range(N-2):
        for j in range(i+2,N):
            total_distance_pre = c[y[i]][y[i+1]] + c[y[j]][y[j+1]]
            total_distance_post = c[y[i]][y[j]] + c[y[i+1]][y[j+1]]
            if total_distance_post < total_distance_pre:
                for k in range(math.ceil(((j-1-i)/2))):
                    temp = y[i+1+k]
                    y[i+1+k] = y[j-k]
                    y[j-k] = temp
                y.pop(-1)
                return (1,y)
    y.pop(-1)
    return (0,y)

def TSP_opt2(y,c,d,N,max_iter):
    cost_record = []
    for i in range(max_iter):
        (label,y) = TSP_onestep_opt2(y,c,N)
        cost_record.append(TSP_tour_cost(y,c,d,N))
        if label == 0:
            break
    return (cost_record, y)

for i in range(iters):
    start_time = time.time()

    filename = r"C:\Users\DELL\OneDrive\Máy tính\Test data OpenERP\N_10_K_2.txt"
    N,M,d,c = INP(filename)
    d.insert(0,0)
    V = set(range(N+1))

    customer_permutation = np.random.permutation(N) + 1

    seed_customer = set(customer_permutation[0:M]) 
    other_customer = V - {0} - seed_customer 

    sorted_other_customer = list(other_customer)
    sorted_other_customer.sort(key = lambda x: d[x],reverse= True)

    ''' The other customer is sorted in decreasing order of customer maintenance time'''

    partial_tour = {} 
    for k in range(M):
        partial_tour[k] = [0,list(seed_customer)[k]]

    for i in sorted_other_customer:
        max_tour_cost = []
        for k in partial_tour.keys():
            partial_tour[k].append(i)
            max_tour_cost.append(max([TSP_tour_cost(partial_tour[j],c,d,len(partial_tour[j])) for j in range(M)]))
            partial_tour[k].pop(-1)
        min_index = max_tour_cost.index(min(max_tour_cost))
        partial_tour[min_index].append(i)
        partial_tour[min_index] = TSP_opt2(partial_tour[min_index], c, d, len(partial_tour[min_index]), 1000)[1]
        max_tour_cost = []

    p_cost = [TSP_tour_cost(partial_tour[k],c,d,len(partial_tour[k])) for k in range(M)]

    f = open('res.txt','w')
    f.write(str(M) + '\n')
    for k in range(M):
        partial_tour[k].append(0)
        f.write(str(len(partial_tour[k])) + '\n')
        line = ''
        for i in partial_tour[k]:
            line = line + str(i) + ' '
        f.write(line + '\n')

    end_time = time.time()

    exe_time = end_time - start_time


    results.append(max(p_cost))
    times.append(exe_time)

with open('experiment.txt','w') as f:
    f.write('f_min = ' + str(min(results)) + '\n')
    f.write('f_max = ' + str(max(results)) + '\n')
    f.write('f_avg = ' + str(sum(results)/(len(results))) + '\n')
    f.write('std_dev = ' + str(statistics.stdev(results)) + '\n')
    f.write('t_avg = ' + str(sum(times)/(len(times))))

print(results)
print('f_min =', min(results))
print('f_max =', max(results))
print('f_avg =', sum(results)/(len(results)))
print(times)
print('t_avg =', sum(times)/(len(times)))

