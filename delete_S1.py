import os
import shutil

S2_dates=[]

for folder in os.listdir('s2_zip'):
    S2_dates.append(folder.split("_")[2].split("T")[0])


for folder in os.listdir('s1_zip'):
    date=folder.split("_")[4].split("T")[0]
    if(date not in S2_dates):
        shutil.rmtree('s1_zip/'+folder)
