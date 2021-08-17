import os 
from shutil import copy
import random

#segment file path
input_path = "C:\\seb\\ecg_detection\\segment\\out2"
#random segment file output
output_path = "C:\\seb\\ecg_detection\\segment\\set\\0101_ex2"



pick_num = 70

ann_folder = os.listdir(input_path)
for p in ann_folder:
    src_path = input_path+"\\"+p
    dst_path = output_path+"\\"+p

    os.mkdir(dst_path)
    
    seg = os.listdir(input_path+"\\"+p)
    seg_num = len(seg)

    if seg_num < pick_num:
        ran = random.sample(range(seg_num),seg_num)
    else:
        ran = random.sample(range(seg_num),pick_num)

    for pick in ran:
        copy(src_path+"\\"+seg[pick],dst_path+"\\"+seg[pick])




