
import os

for S1 in os.listdir("data/S1"):
    if("T34UDA" and "CADC" in S1):
        print("To be deleted:"+S1)
        S2=S1.split("colwith_")[1].replace("tif","png")
        for S2f in os.listdir("data/S2"):
            if(S2f==S2):
                print("To be deleted: "+S2f)
