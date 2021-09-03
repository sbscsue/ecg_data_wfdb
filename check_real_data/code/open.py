import matplotlib.pyplot as plt

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

plt.figure(1)
bookmark = 0
plt.subplot(2,1,1)
plt.plot(data[bookmark+0:bookmark+100000])



#대충 셈플링
resampling = 27
re_data = []
print(n)
d = n//27
print(d)
for i in range(d):
    re_data.append(data[i*resampling])


plt.subplot(2,1,2)
plt.plot(re_data[0:3600])
plt.show()
        
   

