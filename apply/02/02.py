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

sys.path.append("C:\\seb\\ecg_detection\\ecg_data_wfdb")
from use.random_file import random_ecg
from use.datamake import ecg_dataframe





def reshape_x(value):
    re=value.to_numpy()
    row,col = re.shape
    re = re.reshape(row,col, 1)

    return re
    
def reshape_y(value):
    number = [0,1,2,3,4]
    label = ['N','S','V','F','Q']

    value = value.replace(label,number)

    re=value.to_numpy()
    row,col = re.shape
    re = re.reshape(row,col, 1)
    return re

random_ecg(500,"C:\\seb\\ecg_detection\\segment\\out2","C:\\seb\\ecg_detection\\segment\\set\\model_01\\02_test")
x ,y = ecg_dataframe("C:\\seb\\ecg_detection\\segment\\set\\model_01\\02_test\\1_all")

x = reshape_x(x)
y = reshape_y(y)


train_percent = 0.7
data_size = len(x)  
bound = int(data_size * train_percent)-1

train_x,test_x = x[:bound],x[bound:]
train_y,test_y = y[:bound],y[bound:]

#for check ecg signal 



#model start
model = Sequential()
model.add(Conv1D(128,6,input_shape=[288,1],activation='relu'))
model.add(MaxPooling1D(pool_size=2))
model.add(Conv1D(128,6,activation='relu'))
model.add(MaxPooling1D(pool_size=2))
model.add(Flatten())
model.add(Dense(5,activation='softmax'))

model.compile(loss='sparse_categorical_crossentropy' ,optimizer='adam',metrics=['accuracy'])
model.fit(train_x,train_y,epochs=20)
model.save("C:\\seb\\ecg_detection\\ecg_data_wfdb\\00_data\\model\\02_model.h5")

results = model.evaluate(test_x,test_y)
print("test loss, test acc:", results)


#model.compile()

