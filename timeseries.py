import os
from datetime import datetime, timedelta


AOI="T33UWU"
dire="test_data"

days_between=[]
target_dates_2020=[]
target_dates_2019=[]
for filename in os.listdir(dire+"/with_history/S2"):
  if(AOI in filename and "2020" in filename):
    d1s=filename.split("_")[1]
    if(d1s not in target_dates_2020):
      target_dates_2020.append(d1s)
  if(AOI in filename and "2019" in filename):
    d1s=filename.split("_")[1]
    if(d1s not in target_dates_2019):
      target_dates_2019.append(d1s)

target_dates_2020.sort(reverse=True)
target_dates_2019.sort(reverse=True)


tiles=[]
for i in range(len(target_dates_2020)):
  if(i==2):
    for filename in os.listdir(dire+"/with_history/S2"):
      if(target_dates_2020[i] in filename):
        tile=filename.split("_")[5]+"_"+filename.split("_")[6]
        tiles.append(tile)
    print(target_dates_2020[i]+" "+str(len(tiles)))
  j=0
  for filename in os.listdir(dire+"/with_history/S2"):
    for tile in tiles:
      if(target_dates_2020[i] in filename.split("_")[1] and tile in filename):
        j+=1
  print(target_dates_2020[i]+" "+str(j))
  
  
print("")
print("2020")
print("")

tiles=[]
for i in range(len(target_dates_2019)):
  if(i==0):
    for filename in os.listdir(dire+"/with_history/S2"):
      if(target_dates_2019[0] in filename):
        tile=filename.split("_")[5]+"_"+filename.split("_")[6]
        tiles.append(tile)
    print(target_dates_2019[0]+" "+str(len(tiles)))
  j=0
  for filename in os.listdir(dire+"/with_history/S2"):
    for tile in tiles:
      if(target_dates_2019[i] in filename.split("_")[1] and tile in filename):
        j+=1
  print(target_dates_2019[i]+" "+str(j))
                                                                         
    


    

