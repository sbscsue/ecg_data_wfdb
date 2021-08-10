import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 


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
        value = np.empty(sample.size)
   
        for i in range(sample.size):
            value[i] = self.record[sample[i]]
        
        tmp = np.stack((sample,symbol,value),axis=1)
        


        beat = np.empty([])
        non_beat = np.empty([])


        for i in range(len(symbol)):
            if symbol[i] in beat_annotations:
                beat = np.append(beat,tmp[i])
            else:
                non_beat = np.append(non_beat,tmp[i])
        print(beat)
        print(beat.T)
        
        return beat,non_beat
        
    
    '''
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
    '''         
    
    