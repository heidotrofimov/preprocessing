import os
from shutil import copyfile

copied=[]

for filename in os.listdir("s1_tiles/"):
  corresponding_s2=filename.split("colwith_")[1].split(".")[0]
  for filename2 in os.listdir("s2_NDVI"):
    s2name=filename2.split(".")[0]
    if(s2name==corresponding_s2):
      copyfile("s1_tiles/"+filename,"data/S1/"+filename)
      if(filename2 not in copied):
        copyfile("s2_NDVI/"+filename2,"data/S2/"+filename2)
        copied.append(filename2)
      
      
    
