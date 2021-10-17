
import os

for S2 in os.listdir("data/S2"):
    S21=S2.replace("png","tif")
    cond=False
    for S1 in os.listdir("data/S1"):
        S2e=S1.split("colwith_")[1]
        if(S21==S2e):
            cond=True
    if(cond==False):
        print("To be deleted: "+S2)
        os.system("rm data/S2/"+S2)
        
for S2 in os.listdir("data/with_history/S2"):
    S21=S2.replace("png","tif")
    cond=False
    for S1 in os.listdir("data/with_history/S1"):
        S2e=S1.split("colwith_")[1]
        if(S21==S2e):
            cond=True
    if(cond==False):
        print("To be deleted: "+S2)
        os.system("rm data/with_history/S2/"+S2)
        
'''
for S2 in os.listdir("data/S2_RGB"):
    S21=S2.replace("png","tif")
    cond=False
    for S1 in os.listdir("data/S1"):
        S2e=S1.split("colwith_")[1]
        if(S21==S2e):
            cond=True
    if(cond==False):
        print("To be deleted: "+S2)
'''        
        
for S1 in os.listdir("data/S1"):
    S2e=S1.split("colwith_")[1].replace("tif","png")
    cond=False
    for S2 in os.listdir("data/S2"):
        if(S2==S2e):
            cond=True
    if(cond==False):
        print("To be deleted: "+S1)
