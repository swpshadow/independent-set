import random
#chromosome with 10 verts ex: [1, 0, 1, 1, 0, 0, 0, 0, 1, 1]
class DataSet:
    def init(self, size = 10):
        self.data = []
        self.size = size
        self.read_data()

    def fitness(self, chromosome):
        if self.is_feasable(chromosome):
            return sum(chromosome) #since binary this is the number of vertexes included.
        else:
            return -1

    def is_feasable(self, chromosome):
        for curr_vert in range(0,len(chromosome)):
            if chromosome[curr_vert] == 1:
                for prev_vert in range(0, curr_vert):
                    if chromosome[prev_vert] == 1 and self.data[curr_vert][prev_vert] == 1:
                        return False
        return True

    def fix_up(self, chromosome):
        ones = [x for x in range(0,len(chromosome)) if chromosome[x] == 1]
        random.shuffle(ones)
        while not self.is_feasable(chromosome):
            chromosome[ones.pop()] = 0
        return chromosome

    #reads in data to 2d list
    #reads in a data file with this many vertexes
    def read_data(self):
        with open("data//independent_set_{}".format(self.size), 'r') as file:
            for line in file:
                self.data.append([int(x) for x in line.rstrip().split(',')])
        file.close()
