from independent_set import DataSet
import random
import sys

def roulette_selection(pool, data_set):
    probs = []
    sum = data_set.sum_pool_fitness(pool)
    for idx in range(0, len(pool)):
        probs.append(data_set.fitness(pool[idx])/sum)
    return list(random.choices(pool, k=len(pool), weights=probs))


def tournament_selection(pool, data_set, prob = 0.75):
    parent_pool = []
    while len(parent_pool) < len(pool):
        p = random.choices(pool, k=2)
        if random.random() < prob:
            parent_pool.append(p[data_set.best_in_pool(p)[0]])
        else:
            parent_pool.append(p[(data_set.best_in_pool(p)[0]+1) % 2])
    assert len(parent_pool) == len(pool)
    return parent_pool

def cross_over(pool, chromosome_size, crossover = None):
    if crossover is None:
        crossover = uniform_cross_over #so crossover can be optional
    child_pool = []
    c1, c2 = [], []
    for x in range(0, int(len(pool)/2)):
        c1, c2 = crossover(pool[random.randint(0, len(pool)-1)], pool[random.randint(0, len(pool)-1)], chromosome_size)
        child_pool.extend([c1,c2])
    return child_pool

def single_point_crossover(p1, p2, size):
    rand = random.randint(1, size)
    c1 = p1[:rand]
    c1.extend(p2[rand:])
    c2 = p2[:rand]
    c2.extend(p1[rand:])
    assert len(c1) == len(p1) and len(c2) == len(p2)
    return (c1, c2)

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

set_size = 100
pool_size = 60 #make even number
file_name = 'contrived'
if len(sys.argv) > 1:
    file_name = sys.argv[1]
    set_size = int(sys.argv[1])
    pool_size = int(set_size * .6)
    if pool_size % 2 == 1:
        pool_size += 1

data_set = DataSet(file_name, size = set_size)
pool = data_set.random_pool(pool_size)
best = (pool[0], data_set.fitness(pool[0]))

iterations = 0
max_iterations = 12000
since_change = 0
max_not_changed = 5000
#runs until max iterations or it hasn't changed in max_not_changed steps
while iterations < max_iterations and since_change < max_not_changed:
    elites = []
    for _ in range(0,2): #always just 2 elites. They are pulled out of parent pool and put back into next gen.
        b = data_set.best_in_pool(pool)
        elites.append(pool.pop(b[0]))
    parent_pool = tournament_selection(pool, data_set) #roulette_selection(pool, data_set)
    child_pool = cross_over(parent_pool, set_size, single_point_crossover) #can pass which cross to use. Single or uniform
    child_pool = mutation(child_pool) #just the one mutation method because it is a bit string...

    for id in pool: #deals with infeasibles
        data_set.fix_up(id)
    pool = child_pool
    pool.extend(elites) #readds the elites to the population
    new_best = data_set.best_in_pool(pool)
    if new_best[1] > best[1]: #if found something with better fitness, replace best found so far
        best = (pool[new_best[0]], new_best[1])
        since_change = 0
    iterations += 1
    since_change += 1
print(iterations, best)
