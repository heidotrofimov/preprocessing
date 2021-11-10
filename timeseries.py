import os
from datetime import datetime, timedelta


AOI="T33UWU"
dire="test_data"

tiles_of_interest=[]
tiles_file=open("T33UWU_tiles_with_fields.txt","r")
lines=tiles_file.readlines()
for line in lines:
    tiles_of_interest.append(line.rstrip())
tiles_file.close()


target_dates_2020.sort(reverse=True)

for tile in tiles_of_interest:
  count=0
  for filename in os.listdir(dire+"/with_history/S2"):
    if(AOI in filename and tile==filename.split("_")[-2]+"_"+filename.split("_")[-1].split(".")[0]):
      count=count+1
  print(tile+" "+str(count))
  




                                                                         
    


    

