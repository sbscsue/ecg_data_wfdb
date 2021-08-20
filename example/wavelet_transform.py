import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 

import os 
import sys
import pickle 

import wfdb 
import pywt as wt

sys.path.append(os.getcwd())
import use.segment.open as so


path="C:\\seb\\ecg_detection\\segment\\01)no_processing\\out2\\F\\109_49.txt"
ecg= so.file_open(path)


plt.plot(ecg['record'])