#%%

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 

import pathlib as pthl
import os
from os import getcwd,listdir
from os.path import abspath
from pathlib import Path
import sys
import time


home_path = abspath(getcwd())
git_path = home_path+"\\ecg_data_wfdb"

sys.path.append(git_path)
import use.mitbih_ecg.form as es



input_path = abspath(home_path+"\mit_bih")
output_path = abspath(home_path+"\save")

files = listdir(input_path)
for f in files:
    if f.endswith(".dat"):
        start_time = time.time()

        name = f.split(".")
        ecg = es.ecg_segment(input_path,name[0])
        print(ecg.file_path)
        ecg.output_segment(output_path)

        end_time = time.time()
        print("Process Time: ${2}".format(end_time-start_time))
        print(name[0]+" "+"finish")


# %%

# %%
