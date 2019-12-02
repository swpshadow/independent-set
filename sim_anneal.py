from independent_set import DataSet
import random
import sys
import math
import time

def perturb(s):
    u = [1 if random.random() < 0.5 else 0 for _ in range(len(s))]
    new_s = s
    for i in range(0, len(s)):
        if random.random() < 0.2:
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
temp = 500

inner_iterations = 10
beta = 1.03
alpha = .98

start_time = time.time()
while time.time() - start_time < 30:
    for _ in range(0, int(inner_iterations)):
        new_s = perturb(s)
        if data_set.fitness(new_s) < data_set.fitness(s) or random.random() < math.exp((data_set.fitness(s) - data_set.fitness(new_s))/temp):
            s = new_s
    temp *= alpha
    inner_iterations *= beta

print(temp, inner_iterations, s, data_set.fitness(s))
