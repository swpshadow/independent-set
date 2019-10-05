import random
import csv
import sys

numFiles = 1
if len(sys.argv) > 1:
    numFiles = int(sys.argv[1]) #number of files to make
prob = .5
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
