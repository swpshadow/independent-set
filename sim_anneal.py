from independent_set import DataSet
import random
import sys
import math
import time

def perturb(s):
    new_s = [x for x in s]
    rand = random.randint(0, len(s) - 1)
    new_s[rand] = (s[rand] + 1) % 2
    return new_s

def rand_perturb(s):
    new_s = [x for x in s]
    for i in range(0, random.randint(0, int(len(s)-1))):
        if random.random() < 0.01:
            new_s[i] = (s[i] + 1) % 2
    return new_s

def kick(s):
    new_s = [x for x in s]
    for i in range(0, len(s)):
        if random.random() < 0.1:
            new_s[i] = random.choice([0, 1])
    return new_s

set_size = 150
file_name = 'contrived150'
optimal = 51
if len(sys.argv) > 1:
    file_name = sys.argv[1]
    set_size = int(sys.argv[1])

data_set = DataSet(file_name, size = set_size)
s = [1 if random.random() < 0.5 else 0 for _ in range(0,set_size)]
s = data_set.fix_up(s) #initial solution


total_perts = 0
avg_perts = 0
fit = 0
best_fit = 0
t = 0
print(time.time())
for i in range(0,5):
    inner_iterations = 0
    total_perts = 0
    temp = 50
    inner_iterations = 100
    beta = 1.01
    #beta = 1.001/1.01
    alpha = .985
    best = [1 if random.random() < 0.5 else 0 for _ in range(0,set_size)]
    since_improvement = 0
    start_time = time.time()

    while time.time() - start_time < 600 and data_set.fitness(best) < optimal:
        for _ in range(0, int(inner_iterations)):
            total_perts += 1
            new_s = data_set.fix_up(rand_perturb(s)) #rand_perturb
            if data_set.fitness(new_s) > data_set.fitness(s) or random.random() < math.exp(-abs(data_set.fitness(s) - data_set.fitness(new_s))/temp):
                s = [x for x in new_s]
            if data_set.fitness(s) > data_set.fitness(best):
                best = [x for x in s]
                since_improvement = 0
            if since_improvement >= 500:
                s = data_set.fix_up(kick(s))
                since_improvement = 0
        since_improvement += 1
        temp = max(temp*alpha, 1)
        inner_iterations *= beta
    avg_perts += total_perts
    print("final temp: ", temp, "num iterations: ", inner_iterations,"best fit: ", data_set.fitness(best))
    if data_set.fitness(best) > best_fit:
        best_fit = data_set.fitness(best)
    fit += data_set.fitness(best)
    t += time.time() - start_time
    print("time: ", time.time() - start_time)
print("")
print("avg time: ", t/5)
print("best fit: ", best_fit, "avg fit:", fit / 5.0, "avg perts: ", avg_perts/5)
