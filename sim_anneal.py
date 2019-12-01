from independent_set import DataSet
import random
import sys
import math


def perturb(s):
    pass

set_size = 100

if len(sys.argv) > 1:
    file_name = sys.argv[1]
    set_size = int(sys.argv[1])

data_set = DataSet(file_name, size = set_size)
s = [1 if random.random() > 0.5 else 0 for _ in range(0,set_size)]
s = data_set.fix_up(s) #initial solution
temp = 5

inner_iterations = 5
beta = 1.03
alpha = .985
iterations = 0
max_iterations = 8000

while iterations < max_iterations:
    for _ in range(0, inner_iterations):
        new_s = perturb(s)
        new_s = data_set.fix_up(new_s)
        if data_set.fitness(new_s) < data_set.fitness(s) or random.random() < math.exp((data_set.fitness(s) - data_set.fitness(new_s))/temp):
            s = new_s
    temp *= alpha
    inner_iterations *= beta
