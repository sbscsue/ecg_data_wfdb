from genericpath import isdir
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 

import os
from os import makedirs
from os.path import isdir

import sys
import pickle 

import wfdb 


#annotation code 
#https://archive.physionet.org/physiobank/annotations.shtml


#lbbb rbbb 제외
class ecg_segment:
    def __init__( self, file_path, ver="mitbih", channel=[0] , seg_size=144 ,sampto=None):
        # / -> m (저장 문제로)
        self.mit_bih = ['L','N','R','S','E','A','J',
                        'V','F','/','Q',
                        'e','a','j','f']   
        self.aami = { 
                        'N':['L','N','R','e','j'],
                        'S':['A','J','S','a'],
                        'V':['E','V'],
                        'F':['F'],
                        'Q':['/','f','Q']
                        }
        self.binary = {
            'normal': ['N'],
            'abnormal': ['A','a','J','S','V','r','F','e','j','n','E','f'],
            'unclassification':['Q','?']
        }
                        

        self.ver = ver
        if(ver not in ['aami','mitbih','binary']):
            raise NameError('not support annotation')
        self.file_name = file_path.split("\\")[-1]
        self.file_path = file_path

        print(self.file_name)

        self.record = wfdb.rdsamp(self.file_path,channels=channel,sampto = sampto)[0].flatten()
        #annotation  = annotation wfdb class / sample / symbol / value 
        self.annotation = wfdb.rdann(self.file_path,'atr',summarize_labels=True,sampto = sampto)
    

        self.tmp = self.re_ann()
        self.beat , self.non_beat = self.set_annotation()
        self.seg = self.set_segment(seg_size)
    
    
        

    #ecg
    #plot ecg 
    def plot_record(self):
        plt.plot(np.arange(self.get_record().size),self.get_record())
        
    #plot ecg,annotation
    def plot_all(self):
        plt.plot(np.arange(self.get_record().size),self.get_record(),self.get_annotation()[0],self.get_annotation()[2],"o")
    

    #output_segment
    def output_segment(self,dir):
        if self.ver=='aami':
            self.output_segment_aami(dir)
        elif self.ver=='mitbih':
            self.output_segment_mitbih(dir)
        else:
            raise NameError('not support annotation')   




    def re_ann(self):
        n = len(self.annotation.sample)

        sample = self.annotation.sample
        symbol = self.annotation.symbol
        value = np.empty(n)
        

        #(rpeak 값 추출)
        for i in range(n):
            value[i] = self.record[sample[i]]
        
        tmp = np.stack((sample,symbol,value),axis=1)

        return tmp

    #set 
    def set_annotation(self):
        beat = np.empty([])
        non_beat = np.empty([])

        n = len(self.tmp)
        cnt = 0

        tmp = self.tmp

        if self.ver=='aami':   
            tmp = self.tmp
            for i in range(n):
                if tmp[i][1] in self.mit_bih:
                    for j in self.aami:
                        if tmp[i][1] in self.aami[j]:
                            tmp[i][1] = j
                            beat = np.append(beat,tmp[i])
                else:
                    non_beat = np.append(non_beat,tmp[i])
        elif self.ver=='mitbih':
            for i in range(n):
                if tmp[i][1] in self.mit_bih:
                    if tmp[i][1] == "/":
                        tmp[i][1] = "m"
                        beat = np.append(beat,tmp[i])
                    else:
                        beat = np.append(beat,tmp[i])
                else:
                    non_beat = np.append(non_beat,tmp[i])

        elif self.ver == 'binary':
            for i in range(n):
                if tmp[i][1] in self.mit_bih:
                    for j in self.binary:
                        if tmp[i][1] in self.binary[j]:
                            tmp[i][1] = j
                            beat = np.append(beat,tmp[i])
                else:
                    non_beat = np.append(non_beat,tmp[i])

        beat = beat[1:].reshape(-1,3)
        non_beat = non_beat[1:].reshape(-1,3)
        
        return beat,non_beat

 

    def set_segment(self,window):
        segment = []
        
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

    
        
#mitbih 파일 경로 겹치는 오류 
    def output_segment(self,path,img = False):
        ann = []
        if self.ver=='mitbih':
            ann = self.mit_bih
        elif self.ver=='aami':
            ann = list(self.aami.keys())
        elif self.ver == 'binary':
            ann = list(self.binary.keys())


        #type1:101,102
        path1 = path+"\\"+"files"+"\\"+str(self.file_name)
        path1_1 = path1+"\\"+"all"
        path1_2 = path1+"\\"+"ann"
        if isdir(path1) == False:
            makedirs(path1_1)
            for p in ann:
                makedirs(path1_2+"\\"+p)
        

        #type2:n,s,q,r...
        path2 = path+"\\"+"annotation"
        if isdir(path2) == False:
            for p in ann:
                makedirs(path2+"\\"+p+"\\csv")
                if(img == True):
                    makedirs(path2+"\\"+p+"\\img")

        
        for i in range(len(self.seg)):
            record = self.seg[i]['record']
            ann = self.seg[i]['annotation']
            
            data = np.append(record,ann)
            data = pd.DataFrame(data)

            name = str(self.file_name)+"_"+str(i)+".csv"

            data.to_csv(path1_1+"\\"+name,index=False)
            data.to_csv(path1_2+"\\"+ann+"\\"+name,index=False)
            data.to_csv(path2+"\\"+ann+"\\"+"csv"+"\\"+name,index=False)

            if(img == True):
                plt.plot(record)
                plt.savefig(path2+"\\"+ann+"\\"+"img"+"\\"+name+".jpg")
                plt.cla() 

            



            
    

        

        



    
