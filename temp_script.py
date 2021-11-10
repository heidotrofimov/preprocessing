import os

for filename in os.listdir("s2_NDVI"):
    if(len(filename.split("_"))==2):
       os.system("rm s2_NDVI/"+filename)
       
for filename in os.listdir("s2_RGB"):
    if(len(filename.split("_"))==2):
       os.system("rm s2_RGB/"+filename)
    
