
import os

for S1 in os.listdir("test_data/S1"):
    if("T34UDA" and "CADC" in S1):
        os.system("rm test_data/S1/"+S1)
        S2=S1.split("colwith_")[1].replace("tif","png")
        for S2f in os.listdir("test_data/S2"):
            if(S2f==S2):
                os.system("rm test_data/S2/"+S2f)           
    if("T34UDA" and "D103" in S1):
        os.system("rm test_data/S1/"+S1)
        S2=S1.split("colwith_")[1].replace("tif","png")
        for S2f in os.listdir("test_data/S2"):
            if(S2f==S2):
                os.system("rm test_data/S2/"+S2f)
