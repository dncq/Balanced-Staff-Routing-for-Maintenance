import random
n = int(input())
c = [[int(10*random.random())+1 for i in range(n+1)]for j in range(n+1)]
for i in range(n+1):
    c[i][i] = 0
def twooptSwap(route,i,j):
    new_route=[]
    new_route=route[:i+1]+route[j:i:-1]+route[j+1:]
    return new_route
def tour_path_cost(path):  
    l=len(path)
    cost=c[0][path[0]]+c[path[l-1]][0]
    for j in range(1,l-2):
        cost+=c[j][j+1]
    return cost
def inipath(n):
    x=list(range(1,n+1))
    random.shuffle(x)
    route=[0]+x+[0]
    return route
def update(new_route,new_cost):
    return new_route,new_cost
route= inipath(n)
best_cost=tour_path_cost(route)
def MAIN(route,best_cost,n):
 while True:
    for i in range(1,n-2):
        for j in range(i+1,n):
            new_route=twooptSwap(route,i,j)
            new_cost=tour_path_cost(new_route)
            if new_cost<best_cost:
                route,best_cost=update(new_route,new_cost)
                break
for i in range(10):
    MAIN(route,best_cost,n)
print(route,best_cost)
