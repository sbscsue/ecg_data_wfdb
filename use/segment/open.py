import os

import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

from os import listdir

#file open one file 
def ecgtodf(path):

    dir = listdir(path)


    all = np.ndarray(1)
    n=0

    for p in dir:
        print(p)
        data = pd.read_csv(path+"\\"+p,header=None)
        all =  np.append(all,data)
        n = n+1
    all = all[1:]
    all=np.resize(all,(n,289))

    return all

