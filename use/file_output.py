#%%

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import os
from pathlib import Path
import sys

import form as es






#folder = os.path.dirname(os.path.abspath(__file__))
#folder = str(Path(folder).parent.parent)



folder = "C:\\seb\\ecg_detection\\mit_bih"
file = os.listdir("C:\\seb\\ecg_detection\\mit_bih")

for f in file:
    if f.endswith(".dat"):
        name = f.split(".")
        ecg = es.ecg_segment(folder,name[0])
        ecg.output_segment('out1',1)
        ecg.output_segment('out2',2)
        print(name[0]+" "+"finish")


# %%

# %%
