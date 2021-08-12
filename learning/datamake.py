import os
import pickle

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 



def ecg_dataframe(dir):
    record = pd.DataFrame(np.empty((1,288)))
    annotation = pd.DataFrame(np.empty((1,1)))


    for name in os.listdir(dir):
        f = open(dir+"\\"+name,'rb')
        ecg = pickle.load(f)

        r = pd.DataFrame(ecg['record']).T
        a = pd.DataFrame(list(ecg['annotation']))

        record=record.append(r,ignore_index=True)
        annotation=annotation.append(a,ignore_index=True)

    return record[1:],annotation[1:]

