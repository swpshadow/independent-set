import random
import csv
import sys

numFiles = 1
prob = .5
if len(sys.argv) > 1:
    if sys.argv[1] == 'contrived':
        n = 100
        if len(sys.argv) > 2:
            n = int(sys.argv[2])
        l = [[0]*n for _ in range(0,n)]
        for i in range(0, n):
            for j in range(0, n):
                if i == j or (j % 3 == 0 and i % 3 == 0):
                    l[i][j] = 0
                else:
                    l[i][j] = 1
        with open("data//independent_set_contrived", 'w') as csvFile:
            printer = csv.writer(csvFile)
            printer.writerows(l)
        csvFile.close()
        exit(0)
    numFiles = int(sys.argv[1]) #number of files to make
    if len(sys.argv) > 2:
        prob = float(sys.argv[2])

for x in range(1,numFiles + 1, 1):
    n = 10*x
    d = [[0]*n for _ in range(0,n)]

    for i in range(0,n):
        for j in range(0,n):
            if j <= i:
                if d[j][i] == 1:
                    d[i][j] = 1
                else:
                    d[i][j] = 0
            else:
                if random.random() < prob:
                    d[i][j] = 1
                else:
                    d[i][j] = 0

    with open("data//independent_set_{}".format(n), 'w') as csvFile:
        printer = csv.writer(csvFile)
        printer.writerows(d)
    csvFile.close()
