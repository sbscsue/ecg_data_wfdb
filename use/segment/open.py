import os
import pickle


#file open one file 
def file_open(path):
    f = open(path,'rb')
    ecg = pickle.load(f)
    return ecg



#file open all file in folder