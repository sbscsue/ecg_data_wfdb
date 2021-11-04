import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
from sklearn.preprocessing import MinMaxScaler

#dater change to tensor
def to_mixmax_tensor(x,y):
    
    record = x.to_numpy()
    ann = y.to_numpy()
    
    t_record = record.T
    scaler = MinMaxScaler()
    scaler.fit(t_record)
    after_record = scaler.transform(t_record).T


    record = pd.DataFrame(after_record)
    ann = pd.DataFrame(ann)

    x=x_tensor_input(record)
    y=y_tensor_input(ann)

    return x,y

    

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

