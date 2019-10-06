from independent_set import DataSet
import sys

n = 20
if len(sys.argv) > 1:
    n = int(sys.argv[1])
data = DataSet(n)
best = ([1,1,1,1,1,1,1,1,1,1], -1)

for i in range(1 << n):
    s = bin(i)[2:]
    s = '0'*(n-len(s))+s
    perm = list(map(int,list(s)))
    score = data.fitness(perm)
    if score > best[1]:
        best = (perm, score)
print(best)
