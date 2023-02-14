import random
import math
import numpy as np
import matplotlib.pyplot as plt
import sys
import copy
import time
import statistics as sta

#Đọc Dữ liệu

filename = r'C:\Users\VU TUAN MINH\DSA\1.txt'
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
N,K,d,c = INP(filename)
d.insert(0,0)

# Thuật toán 2_Opt

def TSP_tour_cost(y,c,N):
    y.append(y[0])
    cost = 0
    for i in range(N):
        cost += c[y[i]][y[i+1]]
    y.pop(-1)
    return cost

def TSP_tour_cost_1(y,c,d,N):
    y.append(y[0])
    cost = 0
    for i in range(N):
        cost += (c[y[i]][y[i+1]] + d[y[i]])
    y.pop(-1)
    return cost

def TSP_opt2_1(y,c,d,N,max_iter):
    cost_record = []
    for i in range(max_iter):
        (label,y) = TSP_onestep_opt2_1(y,c,N)
        cost_record.append(TSP_tour_cost_1(y,c,d,N))
        if label == 0:
            break
    return (cost_record, y)

def TSP_onestep_opt2_1(y,c,N):
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

def TSP_onestep_opt2(y,c,N):
    y.append(y[0])
    for i in range(N-2):
        for j in range(i+2,N):
            total_distance_pre = c[y[i]][y[i+1]] + c[y[j]][y[j+1]]
            total_distance_post = c[y[i]][y[j]] + c[y[i+1]][y[j+1]]

            if total_distance_post < total_distance_pre:
                for k in range(math.ceil(((j-i-1)/2))):
                    temp = y[i+k+1]
                    y[i+k+1] = y[j-k]
                    y[j-k] = temp
                y.pop(-1)
                return (1,y)
    y.pop(-1)
    return (0,y)

def TSP_opt2(y,c,N,max_iter):
    cost_record = []
    for i in range(max_iter):
        (label,y) = TSP_onestep_opt2(y,c,N)
        cost_record.append(TSP_tour_cost(y,c,N))
        if label == 0:
            break
    return (cost_record, y)

 #Tinh tong chi phi can thiet
 
def Allocating(route_y, Time):
    for i in (route_y):
        Time += d[i]

    return Time

#Hàm đảo 2 đỉnh bất kì trong 1 route

def Swap_Node(i, price1, route1, j, price2, route2): #Dao 2 thanh pho index i, j tren 2 route1 va route2
    route1_copy = copy.deepcopy(route1)
    route2_copy = copy.deepcopy(route2)

    tmp = route1_copy[i]
    route1_copy[i] = route2_copy[j]
    route2_copy[j] = tmp

    route1_index = list(range(len(route1_copy)))
    c_new1 = [[c[i][j] for j in route1_copy] for i in route1_copy]
    cost_record, sub_y1 = TSP_opt2(route1_index, c_new1, len(route1_copy), max_iter)
    route1_cost = cost_record[-1]

    y1 = route1_copy
    index_y1 = sub_y1
    replace_y1 = [0 for x in range (len(y1))]
    for x in range(len(y1)):
        replace_y1[index_y1[x]] = y1[x]
    
    All_Cost_1 = Allocating(replace_y1, route1_cost)

    route2_index = list(range(len(route2_copy)))
    c_new2 = [[c[i][j] for j in route2_copy] for i in route2_copy]
    cost_record, sub_y2 = TSP_opt2(route2_index, c_new2, len(route2_copy), max_iter)
    route2_cost = cost_record[-1]
    
    y2 = route2_copy
    index_y2 = sub_y2
    replace_y2 = [0 for x in range (len(y2))]
    for x in range(len(y2)):
        replace_y2[index_y2[x]] = y2[x]
    
    All_Cost_2 = Allocating(replace_y2, route2_cost)
    if(All_Cost_1 < Lower_Bound or All_Cost_2 < Lower_Bound or abs(All_Cost_1 - All_Cost_2) > Max_ans): 
        return route1, price1, route2, price2
    
    else: return replace_y1, All_Cost_1, replace_y2, All_Cost_2

#Hàm chuyển 1 đỉnh bất kì sang tour khác

def Move_Node(i, price1, route1, price2, route2): # chuyen thanh pho co index i tu route1 sang route2
    route1_copy = copy.deepcopy(route1)
    route2_copy = copy.deepcopy(route2)

    tmp = route1_copy[i]
    route1_copy.remove(tmp)
    route2_copy.append(tmp)

    route1_index = list(range(len(route1_copy)))
    c_new1 = [[c[i][j] for j in route1_copy] for i in route1_copy]
    cost_record, sub_y1 = TSP_opt2(route1_index, c_new1, len(route1_copy), max_iter)
    route1_cost = cost_record[-1]

    y1 = route1_copy
    index_y1 = sub_y1
    replace_y1 = [0 for x in range (len(y1))]
    for x in range(len(y1)):
        replace_y1[index_y1[x]] = y1[x]
    
    All_Cost_1 = Allocating(replace_y1, route1_cost)

    route2_index = list(range(len(route2_copy)))
    c_new2 = [[c[i][j] for j in route2_copy] for i in route2_copy]
    cost_record, sub_y2 = TSP_opt2(route2_index, c_new2, len(route2_copy), max_iter)
    route2_cost = cost_record[-1]
    
    y2 = route2_copy
    index_y2 = sub_y2
    replace_y2 = [0 for x in range (len(y2))]
    for x in range(len(y2)):
        replace_y2[index_y2[x]] = y2[x]
    
    All_Cost_2 = Allocating(replace_y2, route2_cost)
    if(All_Cost_1 < Lower_Bound or All_Cost_2 < Lower_Bound or abs(All_Cost_1 - All_Cost_2) > Max_ans): 
        return route1, price1, route2, price2
    
    else: return replace_y1, All_Cost_1, replace_y2, All_Cost_2

#Thuật toán Greedy để sinh ra trạng thái ban đầu tốt nhất
Route_Record = []
Time_Record = []

for r in range (0, 10):
    V = set(range(N+1))
    Timing_Start = time.time()

    customer_permutation = np.random.permutation(N) + 1

    seed_customer = set(customer_permutation[0:K]) 
    other_customer = V - {0} - seed_customer 

    sorted_other_customer = list(other_customer)
    sorted_other_customer.sort(key = lambda x: d[x],reverse= True)

    ''' The other customer is sorted in decreasing order of customer maintenance time'''

    partial_tour = {} 
    for k in range(K):
        partial_tour[k] = [0,list(seed_customer)[k]]

    for i in sorted_other_customer:
        max_tour_cost = []
        for k in partial_tour.keys():
            partial_tour[k].append(i)
            max_tour_cost.append(max([TSP_tour_cost_1(partial_tour[j],c,d,len(partial_tour[j])) for j in range(K)]))
            partial_tour[k].pop(-1)
        min_index = max_tour_cost.index(min(max_tour_cost))
        partial_tour[min_index].append(i)
        partial_tour[min_index] = TSP_opt2_1(partial_tour[min_index], c, d, len(partial_tour[min_index]), 1000)[1]
        max_tour_cost = []

    p_cost = [TSP_tour_cost_1(partial_tour[k],c,d,len(partial_tour[k])) for k in range(K)]

    max_iter = 100000
    y_cities = []
    Route_y = []

    for x in partial_tour:
        Route_y.append(partial_tour[x])

    #Sap xep cac thanh pho theo cost

    Cities_sorted = []

    for i in range (len(Route_y)):
        Route_x = p_cost[i]
        Cities_sorted.append([Route_x, str(i)])

    Cities_sorted.sort()

    route_index = list(range(N))
    cost_record, sub_y = TSP_opt2(route_index, c, N, max_iter)
    route_cost = cost_record[-1]
    All_Cost = Allocating(route_index, route_cost)

    Lower_Bound = All_Cost / K

    count = 0

    max_iter_1 = 50000

    while(1):
        index_max = int(Cities_sorted[-1][1])
        Price1 = Cities_sorted[-1][0]
        Price2 = Cities_sorted[0][0]
        
        route_max = Route_y[index_max]

        i = int(Cities_sorted[0][1])
        Select = Route_y[i]
        Max_ans = Cities_sorted[-1][0] - Cities_sorted[0][0]

        Cities_sorted.pop(0)
        Cities_sorted.pop(-1)
        index_1 = random.randint(1, len(route_max) - 1)
        index_2 = random.randint(1, len(Select) - 1)


        Route_max, Price1, Select, Price2 = Swap_Node(index_1, Price1, route_max, index_2, Price2, Select)
        Route_y[index_max] = Route_max
        Route_y[i] = Select
        Cities_sorted.append([Price1, str(index_max)])
        Cities_sorted.append([Price2, str(i)])
        Cities_sorted.sort()
        
        count += 1

        if(count > max_iter_1): break

    count = 0

    while(1):
        index_max = int(Cities_sorted[-1][1])
        Price1 = Cities_sorted[-1][0]
        Price2 = Cities_sorted[0][0]
        route_max = Route_y[index_max]
        Max_ans = Cities_sorted[-1][0] - Cities_sorted[0][0]
        i = int(Cities_sorted[0][1])
        Select = Route_y[i]

        Cities_sorted.pop(0)
        Cities_sorted.pop(-1)
        index_1 = random.randint(1, len(route_max) - 1)

        Route_max, Price1, Select, Price2 = Move_Node(index_1,Price1, route_max, Price2, Select)
        Route_y[index_max] = Route_max
        Route_y[i] = Select
        Cities_sorted.append([Price1, str(index_max)])
        Cities_sorted.append([Price2, str(i)])
        Cities_sorted.sort()

        count += 1

        if(count > max_iter_1): break
    
    Timing_End = time.time()
    Route_Record.append(Cities_sorted[-1][0])
    Time_Record.append(Timing_End - Timing_Start)
    

f_max = max(Route_Record)
f_min = min(Route_Record)
f_mean = sta.mean(Route_Record)
f_std = sta.stdev(Route_Record)
t_time = sta.mean(Time_Record)

print(f_max, f_min, f_mean, f_std, t_time)
    




#print(K)
for routes in Route_y:
    routes.append(0)
    print(len(routes))
    print(*routes)
with open('minh_nghien.txt','w') as f:
    f.write(str(K)+'\n')
    # line = ''
    for routes in Route_y:
        f.write(str(len(routes))+ '\n')
        for i in range(len(routes)):
            # line += str(routes[i]) + ' '
            f.write(str(routes[i])+' ')
        f.write('\n')

print(Route_y)
print(Cities_sorted)
print(Timing_End - Timing_Start)