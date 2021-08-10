#%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 


import wfdb 
import neurokit2 as nk

import form as es



folder = 'C:\\0_sebin\\lab\\deep\\wfdb'
file = '100'


ecg = es.ecg_segment(folder,file)
plt.plot(ecg.seg[-1])
plt.show()

# %%
