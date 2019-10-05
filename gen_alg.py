from independent_set import DataSet
import numpy as np
import random

def selection(pool, data_set):
    probs = []
    sum = data_set.sum_pool_fitness(pool)
    for idx in range(0, len(pool)):
        probs.append(data_set.fitness(pool[idx])/sum)
    return list(np.choice(pool, size=len(pool), p=probs))

def cross_over(pool):
    pass

def mutation(pool, mutation_rate = .05):
    for d in pool:
        if random.random() < .05:
            idx = random.randint(0, len(d)-1)
            d[idx] = (d[idx] + 1) % 2 #flips the bit


set_size = 10
pool_size = 10
data_set = DataSet(set_size)
pool = data_set.random_pool(pool_size)
best = (pool[0], data_set.fitness(pool[0]))

for _ in range(0, 5000):
    parent_pool = selection(pool, data_set)

    child_pool = cross_over(parent_pool)

    child_pool = mutation(child_pool)

    for id in pool:
        data_set.fix_up(id)
    pool = child_pool
    new_best = data_set.best_in_pool(pool)
    if new_best[1] > best[1]:
        best = (pool[new_best[0]], new_best[1])

print(best)
