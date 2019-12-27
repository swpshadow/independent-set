from ordered_ind_set import DataSet
import random
import sys
import time


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

def cross_over(pool):
    child_pool = []
    c1, c2 = [], []
    for _ in range(0, int(len(pool)/2)):
        c1, c2 = cross(pool[random.randint(0, len(pool)-1)], pool[random.randint(0, len(pool)-1)])
        child_pool.extend([c1,c2])
    return child_pool

def cross(p1, p2):
    rand = random.randint(1, len(p1))
    c1 = p1[:rand]
    c1.extend(p2[rand:])

    in_child = set(c1)
    contents = set([x for x in range(0, len(c1))])
    left_out = contents.difference(in_child)
    for x in left_out:
        dup = dup_idx(c1)
        if dup == -1:
            break
        c1[dup] = x

    c2 = p2[:rand]
    c2.extend(p1[rand:])

    in_child = set(c2)
    contents = set([x for x in range(0, len(c2))])
    left_out = contents.difference(in_child)
    for x in left_out:
        dup = dup_idx(c2)
        if dup == -1:
            print("oop")
            break
        c2[dup] = x
    return (c1, c2)

def dup_idx(chrom):
    idx = -1
    for i in range(len(chrom)):
        for j in range(i + 1, len(chrom)):
            if chrom[i] == chrom[j]:
                return random.choice([i, j])
    return idx

#single swap mutation
def mutation(pool, mutation_rate):
    for p in pool:
        if random.random() < mutation_rate:
            i1 = random.randint(0,len(p) - 1)
            i2 = random.randint(0,len(p) - 1)
            temp = p[i1]
            p[i1] = p[i2]
            p[i2] = temp
    return pool

set_size = 50 #####################
pool_size = int(.6 * set_size) #make even number
if pool_size % 2 == 1:
    pool_size += 1
file_name = '50' ################################
optimal = 17

if len(sys.argv) > 1:
    file_name = sys.argv[1]
    set_size = int(sys.argv[1])
    pool_size = int(set_size * .6)
    if pool_size % 2 == 1:
        pool_size += 1
print(set_size, pool_size)


avg_fit = 0
best_fit = 0
avg_gens = 0
print(time.time())
for _ in range(0,5):
    data_set = DataSet(file_name, size = set_size)
    # print(data_set.fitness([0, 3, 6, 1, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 9, 2, 4, 5, 7, 8, 10, 11, 13,14, 16, 17, 19, 20, 22, 23, 25, 26, 28, 29, 31, 32, 34, 35, 37, 38, 40, 41, 43, 44, 46, 47, 49]))

    pool = data_set.random_pool(pool_size)
    best = (pool[0], data_set.fitness(pool[0]))
    iterations = 0
    max_iterations = 20000
    since_change = 0
    max_not_changed = 5000

    start_time = time.time()
    #runs until max iterations or it hasn't changed in max_not_changed steps
    while time.time() - start_time < 420 and since_change < max_not_changed and best[1] < optimal:
        elites = []
        for _ in range(0,1): #always just 2 elites. They are pulled out of parent pool and put back into next gen.
            b = data_set.best_in_pool(pool)
            elites.append(pool.pop(b[0]))

        parent_pool = tournament_selection(pool, data_set) 
        child_pool = cross_over(parent_pool) 
        child_pool = mutation(child_pool, mutation_rate = 0.15) 
        pool = child_pool

        pool.extend(elites) #readds the elites to the population
        new_best = data_set.best_in_pool(pool)
        if new_best[1] > best[1]: #if found something with better fitness, replace best found so far
            best = (pool[new_best[0]], new_best[1])
            since_change = 0
        iterations += 1
        since_change += 1

        if best[1] > best_fit:
            best_fit = best[1]
    avg_gens += iterations
    print("num gens: ", iterations, "total time: ", time.time() - start_time)
    print("best fit: ", best[1])
    avg_fit += best[1]
print()
print("best fit: ", best_fit, "avg gens: ", avg_gens / 5, "avg fit: ", avg_fit / 5)
