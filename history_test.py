import os
from datetime import datetime, timedelta

history=[]

for S2 in os.listdir("data/S2"):
  histories=[]
  histories.append(S2)
  AOI=S2.split("_")[2]
  tile=S2.split(AOI+"_")[1]
  date_str=S2.split("_")[1].split("T")[0]
  date_obj=datetime(int(date_str[0:4]),int(date_str[4:6]),int(date_str[6:8]))
  for S2_2 in os.listdir("data/S2"):
      AOI2=S2_2.split("_")[2]
      tile2=S2_2.split(AOI2+"_")[1]
      date_str2=S2_2.split("_")[1].split("T")[0]
      date_obj2=datetime(int(date_str2[0:4]),int(date_str2[4:6]),int(date_str2[6:8]))
      if(AOI2==AOI and tile2==tile and date_obj2<date_obj and date_str2[0:4]==date_str[0:4])):
        histories.append(S2_2)
  if(len(histories)>1):
      history.append(histories)
  
history.sort(key=len)

for i in range(30):
  print(len(history[-(i+1)]))
  print(history[-(i+1)])
    
  
