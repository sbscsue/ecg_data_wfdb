import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 

import os
import sys
import pickle 

import wfdb 

class ecg_segment:
    def __init__( self, file_path, ver="mitbih", channel=[0] ,sampto=None, seg_size=144 ):
        self.mit_bih_ann = ['L','N','R','e','j','A','J','S','a','E','V','F','/','f','Q']   
        self.aami_ann = ['N','S','V','F','Q']
        self.mit_to_aami = { 
                        'N':['L','N','R','e','j'],
                        'S':['A','J','S','a'],
                        'V':['E','V'],
                        'F':['F'],
                        'Q':['/','f','Q']
                        }

                        
        #1. save default value
        self.ver = ver
        self.file_name = file_path.split("\\")[-1]
        self.file_path = file_path

        print(self.file_name)

        #2. record value , annotation value 
        self.record = wfdb.rdsamp(self.file_path,channels=channel,sampto = sampto)[0].flatten()
        #annotation  = annotation wfdb class / sample / symbol / value 
        self.annotation = wfdb.rdann(self.file_path,'atr',summarize_labels=True,sampto = sampto)
    
        self.tmp = self.re_ann()

        #3. segement
        #divide beat and non_beat(wave form)
        if ver=='aami':
            self.beat,self.non_beat = self.set_annotation_aami()
        elif ver=='mitbih':
            self.beat,self.non_beat = self.set_annotation_mitbih()
        else:
            raise NameError('not support annotation')

        #seg = use beat
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
    def set_annotation_aami(self):
        beat = np.empty([])
        non_beat = np.empty([])

        n = len(self.tmp)
        cnt = 0

        tmp = self.tmp
        for i in range(n):
            if tmp[i][1] in self.mit_bih_ann:
                for j in self.mit_to_aami:
                    if tmp[i][1] in self.mit_to_aami[j]:
                        tmp[i][1] = j
                        beat = np.append(beat,tmp[i])
            else:
                non_beat = np.append(non_beat,tmp[i])
        
        beat = beat[1:].reshape((-1,3))
        non_beat = non_beat[1:].reshape((-1,3))

        return beat,non_beat
    
    def set_annotation_mitbih(self):
        beat = np.empty([])
        non_beat = np.empty([])

        n = len(self.tmp)
        cnt = 0

        tmp = self.tmp
        for i in range(n):
            if tmp[i][1] in self.mit_bih_ann:
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

    
        
#output segment to python dictionary 
    def output_segment_aami(self,dir):
    
        #type1:101,102
        path_1 = dir+"\\type1\\"+self.file
        if not os.path.exists(path_1):
            os.makedirs(path_1)
        
        if not os.path.exists(path_1+"\\N"):
            for p in self.aami_ann:
                os.makedirs(path_1+"\\"+p)
        

        #type2:n,s,q,r...
        path_2 = dir+'\\type2'
        if not os.path.exists(path_2):
            os.makedirs(path_2)
        if not os.path.exists(path_2+"\\N"):
            for p in self.aami_ann:
                os.makedirs(path_2+"\\"+p)
             
        n = len(self.seg)

        for i in range(n):
            record = self.seg[i]['record']
            ann = self.seg[i]['annotation']

            data =  pd.DataFrame(np.append(record,ann))
            
            name = str(self.file)+"_"+str(ann)+"_"+str(i)
            
            path = path_1+"\\"+ann+"\\"+name+".csv"
            data.to_csv(path,header=False,index=False)
            path = path_2+"\\"+ann+"\\"+name+".csv"
            data.to_csv(path,header=False,index=False)


    
    
    def output_segment_mitbih(self,path):
        p = path+"\\"+str(self.file)
        csv_p = p+"\\"+"csv"
        img_p = p+"\\"+"img"
        
        print(p)
        print(os.path.isdir(p))
        if os.path.isdir(p)==False:
            os.makedirs(csv_p)
            os.makedirs(img_p)
        else:
            return -1

        for i in range(len(self.seg)):
            print(i)
            ann = self.seg[i]['annotation']
            ecg = pd.DataFrame(self.seg[i]['record'])

            ecg.to_csv(csv_p+"\\"+str(ann)+"_"+str(i))
            plt.plot(ecg)
            plt.savefig(img_p+"\\"+str(ann)+"_"+str(i))

            plt.cla() 
        

            
    

        

        



    
