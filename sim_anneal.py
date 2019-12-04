from independent_set import DataSet
import random
import sys
import math
import time

def perturb(s):
    rand = random.randint(0, len(s) - 1)
    s[rand] = (s[rand] + 1) % 2
    return s
    # u = [1 if random.random() < 0.5 else 0 for _ in range(len(s))]
    # new_s = s
    # for i in range(0, len(s)):
    #     if random.random() < 0.2:
    #         new_s[i] = u[i]
    # return new_s

def kick(s):
    u = [1 if random.random() < 0.5 else 0 for _ in range(len(s))]
    new_s = s
    for i in range(0, len(s)):
        if random.random() < 0.3:
            new_s[i] = u[i]
    return new_s

set_size = 50
file_name = 'contrived50'
if len(sys.argv) > 1:
    file_name = sys.argv[1]
    set_size = int(sys.argv[1])

data_set = DataSet(file_name, size = set_size)
s = [1 if random.random() < 0.5 else 0 for _ in range(0,set_size)]
s = data_set.fix_up(s) #initial solution
temp = 20

inner_iterations = 10
beta = 1.01
alpha = .99

best = s
since_improvement = 0

start_time = time.time()
while time.time() - start_time < 100:
    for _ in range(0, int(inner_iterations)):
        new_s = data_set.fix_up(perturb(s))
        if data_set.fitness(new_s) > data_set.fitness(s) or random.random() < math.exp((data_set.fitness(s) - data_set.fitness(new_s))/temp):
            s = new_s
        if data_set.fitness(s) > data_set.fitness(best):
            best = s
            since_improvement = 0
        if since_improvement >= 1000:
            s = data_set.fix_up(kick(s))
            since_improvement = 0
    temp = max(temp*alpha, 1) 
    inner_iterations *= beta

print(temp, inner_iterations, s, data_set.fitness(s), best, data_set.fitness(best))
