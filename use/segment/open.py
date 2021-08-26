import os

import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

from os import listdir

#file open one file 
def file_open(path):

    dir = listdir(path)

    all = np.ndarray(1)
    n=0

    for p in dir:
        print(p)
        data = pd.read_csv(path+"\\"+p)
        all =  np.append(all,data)
        n = n+1
    all = all[1:]
    all=np.resize(all,(n,288))

    return all
file_open("C:\sebin\ecg\pick\model2\\02\\1_all")

