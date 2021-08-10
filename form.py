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
        self.beat,self.non_beat = self.set_annotation()
        self.seg = self.set_segment(2,144)
    
    
    
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
        
    #set 
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
        
        beat = beat[1:].reshape(-1,3)
        non_beat = non_beat[1:].reshape(-1,3)
        

        return beat,non_beat
         
    def set_segment(self,type,window):
        segment = []
        if type==1:
        #window 양으로 자르기
            '''
            size = self.sample.size // window 
            for i in range(size-1):
                segment.append(self.record[window*i:window*(i+1)-1])
            '''
        #window  -sample - window 양으로 자르기 
        elif type==2:
            size = len(self.beat)
            for i in range(size):
                sepfrom = int(self.beat[i][0])-window
                septo = int(self.beat[i][0])+window

                if sepfrom <= 0:
                    continue
                if septo >= len(self.record):
                    break

                anno = self.beat[i][1]
                segment.append(self.record[sepfrom:septo])     
        return segment
    