import numpy as np
import pandas as pd
import sys
from numpy.random import *

def randomselect(filename_i, filename_o, num):
    arr = []

    with open(filename_i) as f:
        l = f.readlines()
        arr.extend(l)

    l = len(arr)
    print(l)

    fw = open(filename_o, 'w')

    for i in np.arange(num):
        r = randint(l)
        #print(arr[r])
        fw.write(arr[r])

    fw.close

def main():
    filename_i = sys.argv[1]
    filename_o = sys.argv[2]
    num = int(sys.argv[3])
    randomselect(filename_i, filename_o, num)

main()
