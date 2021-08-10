import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 

import tensorflow as tf

import wfdb 
import neurokit2 as nk


class ecg_segment:
    def __init__(self,folder_path,file_name,sampto=None):
        self.file_path = folder_path+'\\'+file_name
        
        #record value , annotation value 
        self.record = wfdb.rdsamp(self.file_path,channels=[0],sampto = sampto)[0].flatten()
        self.annotation = wfdb.rdann(self.file_path,'atr',summarize_labels=True,sampto = sampto)
        

        #annotation  = annotation wfdb class / sample / symbol / value 
        

        #self.set_value()
        
        
        #segment
        self.segment = []
    
    #set1
    def set_value(self):
        for i in range(self.sample.size):
            self.value[i] = self.record[self.sample[i]]
    
    #get
    def get_record(self):
        return self.record
  
    def get_annotation(self):
        return [self.sample,self.symbol,self.value]
    
    #plot
    def plot_record(self):
        plt.plot(np.arange(self.get_record().size),self.get_record())
        
    
    def plot_all(self):
        plt.plot(np.arange(self.get_record().size),self.get_record(),self.get_annotation()[0],self.get_annotation()[2],"o")
        
    #set2 
    def set_annotation(self):
        beat_annotations = ['N','L','R','B','A','a','J','S','V','r','F','e','j','n','E','/','f','Q','?']
        none_beat_annotations = ['[','!',']','x','(',')','p','t','u','`','\'','^','|','~','+','s','T','*','D','=','\"','@']
        
        sample = self.annotation.sample
        symbol = self.annotation.symbol
        

        
        
        return sample,symbol,value
        
    
    #segment 
    def set_segment(self,type,window):
        self.segment = []
        if type==1:
        #window 양으로 자르기
            size = self.sample.size // window 
            for i in range(size-1):
                self.segment.append(self.record[window*i:window*(i+1)-1])
        #window  -annotation - window 양으로 자르기 
        elif type==2:
            size = self.annotation.size
            for i in range(size):
                self.segment.append(self.record[self.sample[i]#sizesize)
                
    