import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
from sklearn.preprocessing import MinMaxScaler

#dater change to tensor
def to_mixmax_tensor(x):
    
    t_record = x.T

    scaler = MinMaxScaler()
    scaler.fit(t_record)
    after_record = scaler.transform(t_record).T
    print(after_record.shape)
    return after_record

    


#for aami class
def x_tensor_input(value):
    x=value.astype(float)
    x=x.to_numpy()
    x_row,x_col = x.shape
    x = x.reshape(x_row,x_col, 1)
    return x

number = [0,1,2,3,4]
label = ['N','S','V','F','Q']

def y_tensor_input(value):
    y=value
    y = y.replace(label,number)
    y=y.to_numpy()
    y_row,y_col = y.shape
    y = y.reshape(y_row,y_col, 1)
    return y

