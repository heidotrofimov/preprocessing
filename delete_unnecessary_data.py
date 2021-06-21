import os
import shutil
import sys

deleted=0

for tif in os.listdir("s1_tif_final"):
    S1_short=tif.split("_")[0]+"_"+tif.split("_")[5]+"_"+tif.split("_")[-1].split(".")[0]
    for collocated in os.listdir("collocated"):
        if(collocated.split("_colwith")[0]==S1_short):
            os.remove("s1_tif_final/"+tif)
            break
            

