#%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import os

import wfdb 

import form as es



folder = os.getcwd()+"\\mit_bih"
file = os.listdir(folder)





for f in file:
    if f.endswith(".dat"):
        name = f.split(".")
        ecg = es.ecg_segment(folder,name[0])
        ecg.output_segment('output')
        print(name[0]+" "+"finish")


# %%

# %%
