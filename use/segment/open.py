from ast import Str
import os
from os import listdir
from pathlib import Path

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
def toDataframe_ann(p):
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

def toDataframe_interval(p):
    p1 = p + "\\" + "files"
    dir = sorted(Path(p1).iterdir(), key=os.path.getmtime)

    #초기 작업 (파일 개수 / 배열 초기화)
    n = 0
    exampleFile = None
    for p2 in dir:
        pD = p2 / 'all'
        f = list(Path.iterdir(pD))
        n+=len(f)

        if(p2==dir[-1]):
            exampleFile = pd.read_csv(f[-1])
    
    exampleFile = exampleFile.to_numpy().flatten()
    print(exampleFile)


    #파일 읽기 
    x = np.empty((n,exampleFile.size+2-1),dtype=float)
    y = np.empty(n,dtype=Str)

    cnt = 0
    for p2 in dir:
        print(p2)
        print("====================")
        pD = p2 / 'all'
        pI = p2 / 'interval' 

        fD = list(Path.iterdir(pD))
        fI = list(Path.iterdir(pI))
        fI = pd.read_csv(fI[0]).to_numpy()

        print(len(fD))
        print(fI.size)
        for i in range(len(fD)):
            print(fD[i])
            d = pd.read_csv(fD[i]).to_numpy().flatten()
            x[cnt+i][0:-2] = d[0:-1]
            x[cnt+i][-2:] = fI[i]
            y[cnt+i] = d[-1]
        
        cnt+=len(fD)


    return x,y
        


def toDataframe_interval10(p):
    p1 = p + "\\" + "files"
    dir = sorted(Path(p1).iterdir(), key=os.path.getmtime)

    #초기 작업 (파일 개수 / 배열 초기화)
    n = 0
    exampleFile = None
    for p2 in dir:
        pD = p2 / 'all'
        f = list(Path.iterdir(pD))
        n+=len(f)

        if(p2==dir[-1]):
            exampleFile = pd.read_csv(f[-1])
    
    exampleFile = exampleFile.to_numpy().flatten()
    print(exampleFile)


    #파일 읽기 
    x = np.empty((n,exampleFile.size+10-1),dtype=float)
    y = np.empty(n,dtype=Str)

    cnt = 0
    for p2 in dir:
        print(p2)
        print("====================")
        pD = p2 / 'all'
        pI = p2 / 'interval' 

        fD = list(Path.iterdir(pD))
        fI = list(Path.iterdir(pI))
        fI = pd.read_csv(fI[0]).to_numpy()

        print(len(fD))
        print(fI.size)
        for i in range(len(fD)):
            print(fD[i])
            d = pd.read_csv(fD[i]).to_numpy().flatten()
            x[cnt+i][0:-10] = d[0:-1]
            x[cnt+i][-10:] = fI[i]
            y[cnt+i] = d[-1]
        
        cnt+=len(fD)


    return x,y
        




