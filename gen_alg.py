from independent_set import DataSet
import random
import sys

def selection(pool, data_set):
    probs = []
    sum = data_set.sum_pool_fitness(pool)
    for idx in range(0, len(pool)):
        probs.append(data_set.fitness(pool[idx])/sum)
    return list(random.choices(pool, k=len(pool), weights=probs))

def cross_over(pool, chromosome_size):
    child_pool = []
    c1, c2 = [], []
    for x in range(0, int(len(pool)/2)):
        c1, c2 = uniform_cross_over(pool[random.randint(0, len(pool)-1)], pool[random.randint(0, len(pool)-1)], chromosome_size)
        child_pool.extend([c1,c2])
    return child_pool

def uniform_cross_over(p1, p2, size):
    u = [random.randint(0,1)] * size
    c1 = [p1[x] if u[x] == 0 else p2[x] for x in range(0,size)]
    c2 = [p1[x] if u[x] == 1 else p2[x] for x in range(0,size)]
    return (c1, c2)

def mutation(pool, mutation_rate = .05):
    for d in pool:
        if random.random() < .05:
            idx = random.randint(0, len(d)-1)
            d[idx] = (d[idx] + 1) % 2 #flips the bit
    return pool

set_size = 10
pool_size = 10 #make even number
if sys.argv:
    set_size = int(sys.argv[1])
    pool_size = int(set_size * .5)
    if pool_size % 2 == 1:
        pool_size += 1

data_set = DataSet(size = set_size)
pool = data_set.random_pool(pool_size)
best = (pool[0], data_set.fitness(pool[0]))

for _ in range(0, 10000):
    parent_pool = selection(pool, data_set)

    child_pool = cross_over(parent_pool, set_size)

    child_pool = mutation(child_pool)

    for id in pool:
        data_set.fix_up(id)
    pool = child_pool
    new_best = data_set.best_in_pool(pool)
    if new_best[1] > best[1]:
        best = (pool[new_best[0]], new_best[1])

print(best)
