import os
from os import listdir
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import sys
sys.path.append("C:\\sebin\\lab\\ecg2\\git\\ecg_data_wfdb")
from use.segment.open import all_check,toDataframe

path1 = "C:\\sebin\\lab\\ecg2\\data\\segment\\04_binary_lead2_144\\annotation\\abnormal"
path2 =  "C:\\sebin\\lab\\ecg2\\git\\ecg_data_wfdb\\use\\ex"

@profile
def toDataframe(p):
    path = p+"\\"+"csv"
    dir = listdir(path)
    
    n = len(dir)
    data_n = np.array(pd.read_csv(path+"\\"+dir[0],header=None)[1:]).flatten().size

    x = np.zeros((n,data_n-1),float)
    y = np.array(['a' for _ in range(n)],dtype="object")

    for i in range(len(dir)):
        print(path+"\\"+dir[i])
        d = pd.read_csv(path+"\\"+dir[i],header=None)[1:]
        d = np.array(d).flatten()
        
        n = len(d)
        
        x[i] = d[0:-1]
        y[i] = d[-1]

    x = x.reshape(-1,n-1)
    return x,y

        
        

        
        
abnormal_x,abnormal_y = toDataframe(path1)
print(abnormal_x[-1])