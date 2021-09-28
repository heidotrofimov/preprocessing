import os
import numpy as np
from datetime import datetime, timedelta


#Leiame kõigepealt kõige hilisema

for filename in os.listdir("s1_tiles_previous"):
  if("T32UPG" in filename):
    S2=filename.split("colwith_")[0].split(".")[0]
    found=False
    for filename2 in os.listdir("s2_NDVI"):
      if(filename2.split(".")[0]==S2):
        found=True
        break
    if(found==False):
      print("To be deleted: "+filename)
  
      
  
  
