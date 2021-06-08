import os
from shutil import copyfile

copied=[]

for filename in os.listdir("s2_NDVI/"):
  s2name=filename.split(".")[0]
  for filename2 in os.listdir("s1_tiles"):
    name=filename2.split("colwith_")[1].split(".")[0]
    if(name==s2name):
      if(filename not in copied):
        copyfile("s2_NDVI/"+filename,"data/S2/"+filename)
        copied.append(filename)
      copyfile("s1_tiles/"+filename2,"data/S2/"+filename2)
      
    
