import wfdb as wf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from BaselineRemoval import BaselineRemoval

'''
input 
path  = path+"\\" +name
mitbih data path

output
ecg
ann[2]  0/point 1/annotation

ecg_square  :
threshold 
peak_duration
'''

def getPeak(path,channel=[0]):
    print(path)
    ecg = wf.rdsamp(path,channels=channel)[0].reshape(-1)
    ann = wf.rdann(path,extension="atr")

    baseObj=BaselineRemoval(ecg)
    ecg = baseObj.ZhangFit()
    
    original = ecg
    square = original ** 2

    #threshold 구하기 
    threshold_original = ecg[0:360*10]
    threshold_square = threshold_original **2
    #1
    threshold1 = np.mean(threshold_square)
    threshold1_plot = np.full((3600),threshold1)
    #2
    sums = []
    for i in range(len(threshold_square)):
        if(threshold_square[i]>threshold1):
            sums.append(threshold_square[i])
    threshold2 = np.average(sums)
    threshold2_plot = np.full(3600,threshold2)
    #3
    threshold3 = threshold2 * 2 
    threshold3_plot = np.full(3600,threshold3)

    print(threshold3)



    mode = 0 
    duration =[]
    for i in range(len(square)):
        if mode == 0:
            if(square[i]>threshold3):
                start = i
                mode = 1
        if mode == 1:
            if(square[i]<threshold3):
                end  = i
                duration.append([start,end])
                mode = 0

    plt.cla()
    plt.plot(square)
    plt.plot(threshold1_plot)
    plt.plot(threshold2_plot)
    plt.plot(threshold3_plot)
    for i in duration:
        plt.axvspan(i[0], i[1], color='red', alpha=0.5)

    plt.xlim([0,3600])
    plt.show()
    
    peaks = []
    for i in duration:
        start = i[0]
        end = i[1]
        peaks.append(start+np.argmax(original[start:end]))

    mit_bih_beat = ['L','N','R','S','E','A','J',
                    'V','F','/','Q',
                    'e','a','j','f']   

    beat = []
    for i in range(len(ann.sample)):
        if ann.symbol[i] in mit_bih_beat:
            beat.append(ann.sample[i])
            
    ecg = original
    beat = beat
    ecg_square = square
    threshold = [threshold1,threshold2,threshold3]
    peak_duration = duration
    peak_index = peaks


    
    return ecg,beat ,ecg_square ,threshold, peak_duration ,peak_index