import math
import numpy as np
import matplotlib.pyplot as plt

filename = r"C:\Users\DELL\OneDrive\Máy tính\test_7.txt"
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
N,M,d,c = INP(filename)
d.insert(0,0)
V = set(range(N+1))

def TSP_tour_cost(y,c,d,N):
    y.append(y[0])
    cost = 0
    for i in range(N):
        cost += (c[y[i]][y[i+1]] + d[y[i]])
    y.pop(-1)
    return cost

# def TSP_tour_plot(y,location,N):
#     y.append(y[0])
#     for i in range(N):
#         plt.plot([location[y[i]][0], location[y[i+1]][0]],[location[y[i]][1], location[y[i+1]][1]],'r')
# #     plt.show()
#     y.pop(-1)

# print(TSP_tour_cost(y,c,N))
# TSP_tour_plot(y,location,N)

def TSP_onestep_opt2(y,c,N):
    y.append(y[0])
    for i in range(N-2):
        for j in range(i+2,N):
            total_distance_pre = c[y[i]][y[i+1]] + c[y[j]][y[j+1]]
            total_distance_post = c[y[i]][y[j]] + c[y[i+1]][y[j+1]]
            # print(y[i],y[i+1],y[j],y[j+1],total_distance_pre-total_distance_post)
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

customer_permutation = np.random.permutation(N) + 1
print(customer_permutation)
seed_customer = set(customer_permutation[0:M]) # cái này là m điểm dùng làm tâm các nhóm tour
print(seed_customer)
other_customer = V - {0} - seed_customer # đây là các điểm còn lại 
print(other_customer)

allocating_cost = {} # có thể bỏ qua cái này
for i in other_customer:
    for m in seed_customer:
        allocating_cost[i,m] = min(c[0][i] + c[i][m] + c[m][0], c[0][m] + c[m][i]) + d[i] + d[m] - (c[0][m] + c[m][0])
        allocating_cost[i,m] = round(allocating_cost[i,m]*1000)
# print(allocating_cost)

partial_tour = {} # Tập các partial_solution
for k in range(M):
    partial_tour[k] = [0,list(seed_customer)[k]]

for i in other_customer:
    max_tour_cost = []
    # try_append = [partial_tour[k].append(i) for k in partial_tour.keys()]
    for k in partial_tour.keys():
        partial_tour[k].append(i)
        # partial_tour[k] = TSP_opt2(partial_tour[k], c,d, len(partial_tour[k]), 10000)[1]
        max_tour_cost.append(max([TSP_tour_cost(partial_tour[j],c,d,len(partial_tour[j])) for j in range(M)]))
        partial_tour[k].pop(-1)
    min_index = max_tour_cost.index(min(max_tour_cost))
    partial_tour[min_index].append(i)
    partial_tour[min_index] = TSP_opt2(partial_tour[min_index], c, d, len(partial_tour[min_index]), 1000)[1]
    max_tour_cost = []

p_cost = [TSP_tour_cost(partial_tour[k],c,d,len(partial_tour[k])) for k in range(M)]

# Đoạn này là in kết quả
f = open('res.txt','w')
f.write(str(M) + '\n')
for k in range(M):
    partial_tour[k].append(0)
    f.write(str(len(partial_tour[k])) + '\n')
    line = ''
    for i in partial_tour[k]:
        line = line + str(i) + ' '
    f.write(line + '\n')

print(partial_tour)

print(p_cost) # In chi phí của các tour
print(max(p_cost)) # In thời gian lớn nhất tỏng các tour

# print(allocating_cost)
