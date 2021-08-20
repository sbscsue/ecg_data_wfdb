import os 
from shutil import copy
import random



#pick random ecg by pick num
#save that folder1(sort annotation) folder2(all annotation)
def random_ecg(pick_num,input_folder,output_folder):
    print("random_ecg")
    ann_folder = os.listdir(input_folder)

    out1=output_folder +"\\0_ann"
    out2=output_folder+"\\1_all"

    if(os.path.isdir(out1)==False):
        print("in")
        dst_path_2 = out2
        os.makedirs(dst_path_2)

        for p in ann_folder:
            src_path = input_folder+"\\"+p

            dst_path_1 = out1+"\\"+p
            os.makedirs(dst_path_1)
            
            seg = os.listdir(src_path)
            seg_num = len(seg)

            if seg_num < pick_num:
                ran = random.sample(range(seg_num),seg_num)
            else:
                ran = random.sample(range(seg_num),pick_num)

            for pick in ran:
                copy(src_path+"\\"+seg[pick],dst_path_1+"\\"+seg[pick])
                copy(src_path+"\\"+seg[pick],dst_path_2+"\\"+seg[pick])




def random_ecg_all(pick_num,input_folder,output_folder):
    ann_folder = os.listdir(input_folder)

    output_folder = output_folder + "\\1_all"


    if(os.path.isdir(output_folder)==False):
        dst_path = output_folder
        os.makedirs(dst_path)

        for p in ann_folder:
            src_path = input_folder+"\\"+p
        

            
            seg = os.listdir(input_folder+"\\"+p)
            seg_num = len(seg)

            if seg_num < pick_num:
                ran = random.sample(range(seg_num),seg_num)
            else:
                ran = random.sample(range(seg_num),pick_num)

            for pick in ran:
                copy(src_path+"\\"+seg[pick],dst_path+"\\"+seg[pick])

