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
      S1_history=name
      ref=days(S1_str,history_str)
  if(len(S1_history)>2 and len(S1_target)>2):
    print("")
    print(S2)
    print(S1_target)
    print(S1_history)
  
