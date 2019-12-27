import random
#chromosome with 10 verts ex: [1, 0, 1, 1, 0, 0, 0, 0, 1, 1]
class DataSet:

    def __init__(self, file_name, size = 10):
        self.data = []
        self.file_name = file_name
        self.size = size
        self.read_data()

    #creates a pool of randomly fixed up individuals.

    def random_pool(self, pool_size = 10):
        pool = []
        for _ in range(0, pool_size):
            pool.append(self.fix_up([1 if random.random() < .5 else 0 for _ in range(self.size)]))
        return pool

    #calculates the fitness of a chromosome if feasable
    def fitness(self, chromosome):
        if self.is_feasable(chromosome):
            return sum(chromosome) #since binary this is the number of vertexes included.
        else:
            return -1

    #checks to see if chromosome is feasible
    def is_feasable(self, chromosome):
        for curr_vert in range(0,len(chromosome)):
            if chromosome[curr_vert] == 1:
                for prev_vert in range(0, curr_vert):
                    if chromosome[prev_vert] == 1 and self.data[curr_vert][prev_vert] == 1:
                        return False
        return True

    #randomly changes 1's to 0's until chromosome is feasable
    def fix_up(self, chromosome):
        ones = [x for x in range(0,len(chromosome)) if chromosome[x] == 1]
        random.shuffle(ones)
        while not self.is_feasable(chromosome):
            chromosome[ones.pop()] = 0
        return chromosome

    #sums the fitnesses of all the chromosomes in the pool. used for selection in genetic algs
    def sum_pool_fitness(self, pool):
        sum = 0
        for p in pool:
            sum += self.fitness(p)
        return sum

    #finds the index and fitness value of the best fitness in the pool
    def best_in_pool(self, pool):
        index = 0
        fitness = self.fitness(pool[0])
        for idx in range(1, len(pool)):
            fit = self.fitness(pool[idx])
            if fit > fitness:
                index = idx
                fitness = fit
        return (index, fitness)

    #reads in data to 2d list
    #reads in a data file with this many vertexes
    def read_data(self):
        with open("../data//independent_set_{}".format(self.file_name), 'r') as file:
            for line in file:
                self.data.append([int(x) for x in line.rstrip().split(',')])
        file.close()
