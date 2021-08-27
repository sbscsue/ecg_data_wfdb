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
from use.segment.pick import random_ecg

input_folder = abspath(getcwd()+"\\save\\4beat_remove\\type2")
output_folder = abspath(getcwd()+"\\pick\\model2\\03")
random_ecg(100,input_folder,output_folder)

