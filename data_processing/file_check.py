import os
import pickle


f = open(os.getcwd()+"\\"+"output\\100\\N\\"+"0.txt",'rb')
ecg = pickle.load(f)

print(type(ecg))
print(type(ecg['record']))
print(type(ecg['annotation']))


print(ecg)