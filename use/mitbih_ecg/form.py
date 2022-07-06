from genericpath import isdir
from turtle import right

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
    def __init__( self, file_path, channel=[0] ,ver="mitbih", baseLineRemoveFlag =1, intervalN = 10,leftSegSize=144,rightSegSize = 144, resample_seg_size = -1):
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
        self.leftSegSize = leftSegSize
        self.rightSegSize = rightSegSize
        self.resample_seg_size = resample_seg_size
        self.intervalN = intervalN

        self.file_name = file_path.split("\\")[-1]
        self.file_path = file_path
        print(self.file_name)


        self.record = wfdb.rdsamp(self.file_path,channels=channel)[0].flatten()
        #annotation  = annotation wfdb class / sample / symbol / value 
        self.annotation = wfdb.rdann(self.file_path,'atr',summarize_labels=True)
    
        self.segmentStartIndex = None
        self.segmentEndIndex = None
        self.intervalStartIndex = None
        
        if(ver not in ['aami','mitbih','binary','nsv']):
            raise NameError('not support annotation')


        if baseLineRemoveFlag == 1:
            pass 
        elif baseLineRemoveFlag == 2:
            print("baseline remove")
            baseObj=BaselineRemoval(self.record)
            self.record = baseObj.ZhangFit()

        else:
            raise TypeError("not support baseLineRemoveFlag")



        self.tmp = self.re_ann(self.intervalN,2)
        print("tmp: ",len(self.tmp))

        self.beat , self.non_beat = self.set_annotation()
    
        self.seg = self.set_segment(leftSegSize,rightSegSize)

        print("startIndex,endIndex: ",self.segmentStartIndex," ",self.segmentEndIndex-1)

        print("seg: ",len(self.seg))

        self.interval = self.set_interval(self.segmentStartIndex,self.segmentEndIndex)
        print("interval: ",self.interval.shape)
        #delete
        print("interval value:",self.interval[0])
        
        self.set_segmentIntervalSync(2)
        print("startIndex: ",self.intervalStartIndex," ")
        print("seg,interval: ",len(self.seg)," ",len(self.interval))
       
        
    

    #ecg
    #plot ecg 
    def plot_record(self):
        plt.plot(np.arange(self.get_record().size),self.get_record())
        
    #plot ecg,annotation
    def plot_all(self):
        plt.plot(np.arange(self.get_record().size),self.get_record(),self.get_annotation()[0],self.get_annotation()[2],"o")
    

    def re_ann(self,intervalN,ver):
        if(ver==1):
            n = len(self.annotation.sample)

            sample = self.annotation.sample
            symbol = self.annotation.symbol
            value = np.empty(n)
            prevInterval = np.empty(n)
            averageInterval = np.empty(n)
            

            #(rpeak 값 추출)
            for i in range(n):
                value[i] = self.record[sample[i]]

            #prevInterval값 추출

            for i in range(n):
                flag = i-1
                if(flag<0):
                    prevInterval[i] = -1
                else:
                    cnt = 0
                    for j in range(flag,i):
                        cnt = cnt + (sample[j+1] - sample[j])/360
                    prevInterval[i] = cnt 

            
            #Averageinterval값 추출 
            for i in range(n):
                flag = i-(intervalN)
                if(flag<0):
                    averageInterval[i] = -1
                else:
                    cnt = 0
                    for j in range(flag,i):
                        cnt = cnt + (sample[j+1] - sample[j])/360
                    averageInterval[i] = cnt / 10

            tmp = np.stack((sample,symbol,value,prevInterval,averageInterval),axis=1)

            return tmp

        elif(ver==2):
            n = len(self.annotation.sample)
            sample = self.annotation.sample
            symbol = self.annotation.symbol
            value = np.empty(n)
            prevInterval = np.empty((n,intervalN))
 
            for i in range(n):
                flag = i-(intervalN)
                f = 0
                for j in range(flag,i):
                    if(j<0):
                        prevInterval[i][f] = -1
                    else:
                        cnt = 0
                        cnt = (sample[j+1] - sample[j])/360
                        prevInterval[i][f] = cnt
                    f+=1
            
            tmp = np.stack((sample,symbol,value),axis=1)
            print("tmp1,",tmp.shape)
            tmp2 = np.column_stack([tmp,prevInterval])
            print("tmp2:",tmp2.shape)

            return tmp2
            

        else:
            raise TypeError("not support interval mode")
      


    #set 
    def set_annotation(self):
        beat = np.empty([])
        non_beat = np.empty([])

        n = len(self.tmp)

        tmp = self.tmp[:,0:3]

        if self.ver=='aami':   
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

    
    def set_segment(self,leftWindow,rightWindow):
        segment = []
        
        size = len(self.beat)
        for i in range(size):
            sepfrom = int(self.beat[i][0])-leftWindow
            septo = int(self.beat[i][0])+rightWindow

            if sepfrom <= 0:
                self.segmentStartIndex = i+1
                continue
            if septo >= len(self.record) or (i==(size-1)):
                self.segmentEndIndex = i
                break
            
            if(self.resample_seg_size == -1):
                resample = self.record[sepfrom:septo]
            else:
                resample = signal.resample(self.record[sepfrom:septo],self.resample_seg_size)
                
            segment.append({'record':resample,
                        'annotation':self.beat[i][1]
                        }) 
        return segment

    def set_interval(self,start,end):
        interval = self.tmp[start:end,3:]
        return interval 

    def set_segmentIntervalSync(self,ver):

        if (ver==1):
            indexTmp = None
            for i in range(len(self.interval)):
                if(float(self.interval[i][1]) != -1):
                    indexTmp=i
                    break
            
            self.intervalStartIndex = indexTmp
            
            self.seg = self.seg[self.intervalStartIndex:]
            self.interval = self.interval[self.intervalStartIndex:]
        elif(ver==2):
            indexTmp = None
            for i in range(len(self.interval)):
                if(float(self.interval[i][0]) != -1):
                    indexTmp=i
                    break
            
            self.intervalStartIndex = indexTmp
            
            self.seg = self.seg[self.intervalStartIndex:]
            self.interval = self.interval[self.intervalStartIndex:]

        else:
            raise TypeError("not support interval mode")
        

        
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


    def output_interval(self,path):
        #type1:101,102
        path1 = path+"\\"+"files"+"\\"+str(self.file_name)
        path2 = path1+"\\"+"interval"

        if isdir(path2) == False:
            makedirs(path2)
        
        data = pd.DataFrame(self.interval).astype(float)
        data.to_csv(path2+"\\"+"interval.csv",float_format='%.3f',columns=None,index=None)

        
     
    def returnAllReSampleEcgToString(self,folderPath,resizeFs = -1):
        reEcg = self.record.astype(np.float32)

        if(resizeFs != -1):
            reEcg = resample(self.record,30*60*resizeFs)
        else:
            reEcg = self.record

        pdEcg = pd.DataFrame(reEcg)
        print(pdEcg[0])
        pdEcg.to_csv(folderPath+"\\"+self.file_name+".csv",header=None,index=False,float_format='%.3f')



        

        



            
    

        

        



    
