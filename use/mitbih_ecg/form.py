import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 

import os
import sys
import pickle 

import wfdb 

class ecg_segment:
    def __init__(self,folder_path,file_name,sampto=None):
        #1. save file path
        self.folder = folder_path
        self.file = file_name

        self.file_path = folder_path+'\\'+file_name
        
        #2. record value , annotation value 
        self.record = wfdb.rdsamp(self.file_path,channels=[0],sampto = sampto)[0].flatten()
        #annotation  = annotation wfdb class / sample / symbol / value 
        self.annotation = wfdb.rdann(self.file_path,'atr',summarize_labels=True,sampto = sampto)
        

        #3. segement
        #divide beat and non_beat(wave form)
        self.beat,self.non_beat = self.set_annotation()
        #seg = use beat
        self.seg = self.set_segment(2,144)
        #sample_seg 
        self.sample_seg = None
    
    #get
    def get_record(self):
        return self.record
  
    def get_annotation(self):
        return [self.sample,self.symbol,self.value]
    


    #plot
    #plot ecg 
    def plot_record(self):
        plt.plot(np.arange(self.get_record().size),self.get_record())
        
    #plot ecg,annotation
    def plot_all(self):
        plt.plot(np.arange(self.get_record().size),self.get_record(),self.get_annotation()[0],self.get_annotation()[2],"o")
        
    #set 
    def set_annotation(self):
        beat_annotations = ['N','L','R','B','A','a','J','S','V','r','F','e','j','n','E','/','f','Q','?']
        none_beat_annotations = ['[','!',']','x','(',')','p','t','u','`','\'','^','|','~','+','s','T','*','D','=','\"','@']
        

        mit_to_aami = { 'N':['N','L','R','e','j'],
                        'S':['A','a','J','S'],
                        'V':['V','E'],
                        'F':['F'],
                        'Q':['/','f','Q']
                       }


        sample = self.annotation.sample
        symbol = self.annotation.symbol
        value = np.empty(sample.size)
   
        for i in range(sample.size):
            value[i] = self.record[sample[i]]
        
        tmp = np.stack((sample,symbol,value),axis=1)
        
        

        beat = np.empty([])
        non_beat = np.empty([])

        cnt = 0
        for i in range(len(symbol)):
            if symbol[i] in beat_annotations:
                for j in mit_to_aami:
                    if symbol[i] in mit_to_aami[j]:
                        tmp[i][1] = j
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
                
                
                segment.append({'record':self.record[sepfrom:septo],
                                'annotation':self.beat[i][1]
                                }) 
        return segment
        




#output segment to python dictionary 
#output dir /type1:100,101
    def output_segment(self,dir):
        aami = ['N','S','V','F','Q']

        #type1:101,102
        #type2:n,s,q,r...
        path_1 = dir+"\\type1\\"+self.file
        if not os.path.exists(path_1):
            os.makedirs(path_1)
        if not os.path.exists(path_1+"\\N"):
            for p in aami:
                os.makedirs(path_1+"\\"+p)

        path_2 = dir+'\\type2'
        if not os.path.exists(path_2):
            os.makedirs(path_2)
        if not os.path.exists(path_2+"\\N"):
            for p in aami:
                os.makedirs(path_2+"\\"+p)
             
        n = len(self.seg)

        for i in range(n):
            record = self.seg[i]['record']
            ann = self.seg[i]['annotation']

            data =  pd.DataFrame(np.append(record,ann))
            
            name = self.file+"_"+str(i+1)+".csv"
            data.to_csv(path_1+"\\"+ann+"\\"+name,header=False,index=False)
            data.to_csv(path_2+"\\"+ann+"\\"+name,header=False,index=False)

#upgrade to csv file all 
'''
    #output
    def output_segment(self,dir,ver):
        aami = ['N','S','V','F','Q']

        #파일별로 분류 
        if ver==1:
            path_1 = dir
            if not os.path.exists(path_1):
                os.makedirs(path_1)
            
            path_2 = path_1+"\\"+self.file
            os.makedirs(path_2)

            
            for p in aami:
                os.makedirs(path_2+"\\"+p)
            

            
            n = len(self.seg)

            for i in range(n):
                ann = self.seg[i]['annotation'] 
                f = open(path_2+"\\"+ann+"\\"+self.file+"_"+str(i+1)+".txt",'wb')
                pickle.dump(self.seg[i],f)
                f.close()

        #segnet별로 분류 (고쳐)
        if ver==2:
            path_1 = dir
            if not os.path.exists(path_1):
                os.makedirs(path_1)

            for p in aami:
                if not os.path.exists(path_1+"//"+p):
                    os.makedirs(path_1+"\\"+p)
            
            n = len(self.seg)
            for i in range(n):
                ann = self.seg[i]['annotation'] 
                f = open(path_1+"\\"+ann+"\\"+self.file+"_"+str(i+1)+".txt",'wb')
                pickle.dump(self.seg[i],f)
                f.close()
'''


    


    

        

        



    
