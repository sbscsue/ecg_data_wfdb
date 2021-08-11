#%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 


import wfdb 
import neurokit2 as nk

import form as es



folder = 'C:\\Users\\KIMSEBIN\\Desktop\\2021\\302vacation\\000lab\\deep\\data\\mitdb'
file = '101'


ecg = es.ecg_segment(folder,file)
ecg.output_segment('output')

# %%

# %%
