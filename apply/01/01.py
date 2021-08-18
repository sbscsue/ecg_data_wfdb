import re
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 

import tensorflow as tf
import keras as kr

from keras import Sequential
from keras.layers import Conv1D,MaxPooling1D,Flatten,Dense

import os 
import sys
import pickle 

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

from learning.datamake import ecg_dataframe

def reshape(value):
    re=value.to_numpy()
    row,col = re.shape
    re = re.reshape(row,col, 1)

    return re

x ,y = ecg_dataframe("C:\\seb\\ecg_detection\\segment\\set\\01\\1_train(ann_all)")

x = reshape(x)
y = reshape(y)

x_train ,x_test = x[0:len(x)*0.7]
y_train, y_test = 

#model start
model = Sequential()
model.add(Conv1D(128,6,input_shape=[288,1],activation='relu'))
model.add(MaxPooling1D(pool_size=2))
model.add(Conv1D(128,6,activation='relu'))
model.add(MaxPooling1D(pool_size=2))
model.add(Flatten())
model.add(Dense(5,activation='softmax'))

