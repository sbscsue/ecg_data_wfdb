import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 


from os.path import abspath
from os import listdir
import sys

home_path = "C:\\sebin\\ecg"
git_path = home_path+"\\ecg_data_wfdb"
sys.path.append(git_path)

from use.segment.open import ecgtodf


output_folder = abspath(home_path+"\\pick\\model02\\07\\0_ann")


while(True):
    ann = str(input())
    if ann=='.':
        break
    else:
        if ann in ['N','S','V','F','Q']:
            index = -1
            folder = output_folder+"\\"+ann
            files = listdir(folder)

            n = len(folder)

            while(True):
                check = str(input())
                if check == 'N':
                    if index < n-1:
                        index+=1

                        file = folder+"\\"+files[index]
                        print(file)

                        ecg = pd.read_csv(file,header=None)
                        ecg = ecg[0:-1].to_numpy()
                        ecg = ecg.astype('float')
                        plt.plot(ecg)
                        plt.show()
                        

                    else:
                        print("인덱스가 끝에 있습니다.")
                if check == 'P':
                    if index > 0:
                        index-=1

                        file = folder+"\\"+files[index]
                        print(file)

                        ecg = pd.read_csv(file,header=None)
                        ecg = ecg[0:-1].to_numpy()
                        ecg = ecg.astype('float')
                        plt.plot(ecg)
                        plt.show()
                        
                    else:
                        print("인덱스가 앞에 있습니다.")
                    
                if check == 'O':
                    print("주석 설정창으로")
                    break
                

        else:
            print("종료")
            break


while(True):
    ann = str(input())
    if ann=='.':
        break
    else:
        folder = listdir("C:\\sebin\\lab\\ecg\\save\\mit_ann_all\\type2")
        if ann in folder:
            index = -1
            folder = output_folder+"\\"+ann
            files = listdir(folder)

            n = len(folder)

            while(True):
                check = str(input())
                if check == 'N':
                    if index < n-1:
                        index+=1

                        file = folder+"\\"+files[index]
                        print(file)

                        ecg = pd.read_csv(file,header=None)
                        ecg = ecg[0:-1].to_numpy()
                        ecg = ecg.astype('float')
                        plt.plot(ecg)
                        plt.show()

                    else:
                        print("인덱스가 끝에 있습니다.")
                        break
                if check == 'P':
                    if index > 0:
                        index-=1

                        file = folder+"\\"+files[index]
                        print(file)

                        ecg = pd.read_csv(file,header=None)
                        ecg = ecg[0:-1].to_numpy()
                        ecg = ecg.astype('float')
                        plt.plot(ecg)
                        plt.show()
                    else:
                        print("인덱스가 앞에 있습니다.")
                        break
                    
                if check == 'O':
                    print("주석 설정창으로")
                    break
                

        else:
            print("종료")
            break
        