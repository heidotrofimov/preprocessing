import os

destination="/home/users/biomass/"
home="data/"

folders=["S1/","S2/","S2_RGB/","with_history/S1/","with_history/S2/","with_history/S2_RGB/"]
for folder in folders:
  for filename in os.listdir(home+folder):
    moved=False
    for filename2 in os.listdir(destination+folder):
      if(filename==filename2):
        moved=True
    if(moved==False):
      os.system("cp "+home+folder+filename+" "+destination+folder+filename)
    
    
