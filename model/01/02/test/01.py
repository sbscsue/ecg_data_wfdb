import re
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 

import tensorflow as tf
import keras as kr

from keras import Sequential
from keras.layers import Conv1D,MaxPooling1D,Flatten,Dense

import os 
import sys
import pickle 


sys.path.append("C:\\seb\\ecg_detection\\ecg_data_wfdb")
from use.random_file import random_ecg
from use.datamake import ecg_dataframe



new_model = kr.models.load_model("C:\\seb\\ecg_detection\\ecg_data_wfdb\\00_data\\model\\02_model.h5")
new_model.summary()


