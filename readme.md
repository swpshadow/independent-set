## Independent-set
a program to generate sets and find the largest independent subset using genetic algorithm and simulated annealing.
# how to run:
download sets or generate sets with gen_sets.py.

for gen_alg, ordered_gen_alg, or sim_anneal change the set_size and file name as appropriate (if 50 nodes, filename should be set to '50' and set_size to 50)

parameters such as initial temperature should be changed as wanted to optimize convergence. 

Fitness for all algorithms and chromosomes is the number of nodes in the independent set. 

ordered_gen_alg and ordered_ind_set are a different take on the chromosome. Instead of binary it is order based. Every node is in the chromosome and starting from the left, nodes are 'added' to the independent set until there is a conflict. So [0, 3, 5...] for a contrived set would consider 0, 3 in the independent set but when it tries to add 5 it sees an edge from 5 to 0, so the set is done being built and has a fitness of 2. 
