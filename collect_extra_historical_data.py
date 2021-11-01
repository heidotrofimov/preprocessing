import os
from datetime import datetime, timedelta

def dt(str):
  return datetime(int(str[0:4]),int(str[4:6]),int(str[6:8]))

def days(str1,str2):
  dt1=dt(str1)
  dt2=dt(str2)
  return abs((dt1-dt2).days)

for S2 in os.listdir("data/with_history/S2/"):
  AOI=S2.split("_")[2]
  tile=S2.split("_")[-2]+"_"+S2.split("_")[-1].split(".")[0]
  target_str=S2.split("_")[1].split("T")[0]
  history_str=S2.split("_")[4].split("T")[0]
  target_S1s=[]
  historical_S1s=[]
  S1_target=""
  S1_history=""
  for S1 in os.listdir("data/with_history/S1"):
    S1_str=S1.split("_")[1].split("T")[0]
    AOI2=S1.split("_")[6]
    tile2=S1.split("_")[-2]+"_"+S1.split("_")[-1].split(".")[0]
    if(S1.split("colwith_")[1].split(".")[0]==S2.split(".")[0]):
      target_S1s.append(S1)
    if(AOI==AOI2 and tile==tile2 and (days(S1_str,history_str)==0 or days(S1_str,history_str)==1 or days(S1_str,history_str)==2)):
      historical_S1s.append(S1)
  ref=5
  for name in target_S1s:
    S1_str=name.split("_")[1].split("T")[0]
    if(days(S1_str,target_str)<ref):
      S1_target=name
      ref=days(S1_str,target_str)
  ref=5
  for name in historical_S1s:
    S1_str=name.split("_")[1].split("T")[0]
    if(days(S1_str,history_str)<ref):
      S1_history="data/with_history/S1/"+name
      ref=days(S1_str,history_str)
  if(len(S1_history)<2):
    for S1 in os.listdir("data/S1"):
      S1_str=S1.split("_")[1].split("T")[0]
      AOI2=S1.split("_")[6]
      tile2=S1.split("_")[-2]+"_"+S1.split("_")[-1].split(".")[0]
      if(AOI==AOI2 and tile==tile2 and (days(S1_str,history_str)==0 or days(S1_str,history_str)==1 or days(S1_str,history_str)==2)):
        historical_S1s.append(S1)
      ref=5
      for name in historical_S1s:
        S1_str=name.split("_")[1].split("T")[0]
        if(days(S1_str,history_str)<ref):
          S1_history="data/S1/"+name
          ref=days(S1_str,history_str)
  if(len(S1_history)>2 and len(S1_target)>2):
    new_name=S1_target.split("_colwith")[0]+"_"+S1_history.split("_colwith")[0]+"_colwith_"+S1_target.split("colwith_")[1]
    os.system("cp data/with_history/S2/"+S2+" data/extra_historical/S2/")
    os.system("gdal_merge.py -ot Float32 -of GTiff -separate -o data/extra_historical/S1/"+new_name+" data/with_history/S1/"+S1_target+" "+S1_history)
    print("")
    print("cp data/with_history/S2/"+S2+" data/extra_historical/S2/")
    print("gdal_merge.py -ot Float32 -of GTiff -separate -o data/extra_historical/S1/"+new_name+" data/with_history/S1/"+S1_target+" "+S1_history)
  
