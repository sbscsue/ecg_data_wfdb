import os

import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

from os import listdir

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
    

    df = pd.DataFrame(np.empty((1,289)))
    print(df)
    for f in dir:
        print(path+"\\"+f)
        data = pd.read_csv(path+"\\"+f,header=None)[1:].T
        print(data)
        df.append(df,data)
        
    return df
        



