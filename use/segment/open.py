import os
from os import listdir

import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt


def all_check(path):
    ann = []
    cnt = []
    dir = listdir(path)
    for i in range(len(dir)):
        f = 0
        for j in listdir(path+"\\"+dir[i]+"\\"+"csv"):
            f+=1
        ann.append(dir[i])
        cnt.append(f)
    return ann,cnt

#annotation 별 open _ dtframe ( annotation 별로 저장되어있는 파일로)
#주의 ! data 부분 1번째 배열부터 뽑아옴
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
        



