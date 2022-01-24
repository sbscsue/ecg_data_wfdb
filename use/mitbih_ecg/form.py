from genericpath import isdir

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 

from scipy import signal

import os
from os import makedirs
from os.path import isdir

import sys
import pickle

from BaselineRemoval import BaselineRemoval
from scipy.signal.signaltools import resample 

import wfdb 


#annotation code 
#https://archive.physionet.org/physiobank/annotations.shtml


#lbbb rbbb 제외
class ecg_segment:
    def __init__( self, file_path, channel=[0] ,ver="mitbih", mode =1, seg_size=144, resample_seg_size = -1):
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

        # N : 정상 / S: 심방이전 / V: 심실 
        self.nsv = {
            'N' : ['N'],
            'S' : ['e','A','J','j','S','a'],
            'V' : ['E','V','F']
        }
        
        self.ver = ver
        self.seg_size = seg_size
        self.resample_seg_size = resample_seg_size

        if(ver not in ['aami','mitbih','binary','nsv']):
            raise NameError('not support annotation')
        self.file_name = file_path.split("\\")[-1]
        self.file_path = file_path

        print(self.file_name)

        self.record = wfdb.rdsamp(self.file_path,channels=channel)[0].flatten()
        #annotation  = annotation wfdb class / sample / symbol / value 
        self.annotation = wfdb.rdann(self.file_path,'atr',summarize_labels=True)
    
        
        if mode == 1:
            pass 
        elif mode == 2:
            print("baseline remove")
            baseObj=BaselineRemoval(self.record)
            self.record = baseObj.ZhangFit()

        else:
            raise TypeError("not support mode")

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
        
        elif self.ver == 'nsv':
            for i in range(n):
                if tmp[i][1] in self.mit_bih:
                    for j in self.nsv:
                        if tmp[i][1] in self.nsv[j]:
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
            
            if(self.resample_seg_size == -1):
                resample = self.record[sepfrom:septo]
            else:
                resample = signal.resample(self.record[sepfrom:septo],self.resample_seg_size)
                
            segment.append({'record':resample,
                        'annotation':self.beat[i][1]
                        }) 

            
            

        return segment

    
        
#mitbih 파일 경로 겹치는 오류 
    def output_segment(self,path,img = False):
        print("output")
        ann = []
        if self.ver=='mitbih':
            ann = self.mit_bih
        elif self.ver=='aami':
            ann = list(self.aami.keys())
        elif self.ver == 'binary':
            ann = list(self.binary.keys())
        elif self.ver == 'nsv':
            ann = list(self.nsv.keys())


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


    
   
    def returnAllReSampleEcgToString(self,folderPath,resizeFs = -1):
        reEcg = self.record.astype(np.float32)

        if(resizeFs != -1):
            reEcg = resample(self.record,30*60*resizeFs)
        else:
            reEcg = self.record

        pdEcg = pd.DataFrame(reEcg)
        print(pdEcg[0])
        pdEcg.to_csv(folderPath+"\\"+self.file_name+".csv",header=False,index=False,float_format='%.3f')
        


        

        



            
    

        

        



    
