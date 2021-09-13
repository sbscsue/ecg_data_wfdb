import matplotlib.pyplot as plt
import scipy as sc
import neurokit2 as nk
from scipy.signal import decimate 
import numpy as np

home_path = "C:\\sebin\\ecg"
git_path = home_path+"\\ecg_data_wfdb"

file_path = git_path+"\\check_real_data\\ecg.txt"

data = []

with open(file_path,'r') as f:
    cnt = 0

    f.readline()
    date_time = f.readline()

    while(True):
        line = f.readline()
        if  line == '':
            break
        data.extend(line.rstrip().split("  "))
        cnt+=1

n = len(data)
for i in range(n):
    data[i] = float(data[i])


resampling = 28
print(n)
re_n = n//28
print(re_n)


re_data = []
for i in range(re_n):
    re_data.append(data[i*resampling])
    

index = 5
plt.subplot(3,1,1)
plt.plot(data)

plt.subplot(3,1,2)
plt.plot(re_data)



peak = nk.ecg.ecg_findpeaks(re_data, sampling_rate=360, method='neurokit')
peak = np.array(peak['ECG_R_Peaks'])

peak_y = np.zeros(re_n)
for i in peak:
    peak_y[i] = re_data[i]

re_n = range(re_n)
plt.subplot(3,1,3)
plt.plot(re_n,re_data,re_n,peak_y,"o")
plt.ylim(1000)

plt.show()