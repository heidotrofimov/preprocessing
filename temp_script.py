
import os

for S1 in os.listdir("data/S1"):
    if("T33UWT" and "F363" in S1):
        os.system("rm data/S1/"+S1)
        S2=S1.split("colwith_")[1].replace("tif","png")
        for S2f in os.listdir("data/S2"):
            if(S2f==S2):
                os.system("rm data/S2/"+S2f)           
    if("T33UWT" and "FAA9" in S1):
        os.system("rm data/S1/"+S1)
        S2=S1.split("colwith_")[1].replace("tif","png")
        for S2f in os.listdir("data/S2"):
            if(S2f==S2):
                os.system("rm data/S2/"+S2f)
