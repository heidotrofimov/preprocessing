import os
from datetime import datetime, timedelta

for S1 in os.listdir("data/S1"):
  S1p=S1.split("_colwith")[0]
  parts=S1p.split("_")
  if(len(parts)>3):
    print(S1)
    date=S1.split("_")[7]
    newname=parts[0]+"_"+date+"_"+parts[4]+"_colwith_"+S1.split("colwith_")[1]
    print(newname)
    os.system("mv data/S1/"+S1+" data/S1/"+newname)
    
for S1 in os.listdir("data/with_history/S1"):
  S1p=S1.split("_colwith")[0]
  parts=S1p.split("_")
  if(len(parts)>3):
    print(S1)
    date=S1.split("_")[7]
    newname=parts[0]+"_"+date+"_"+parts[4]+"_colwith_"+S1.split("colwith_")[1]
    print(newname)
    os.system("mv data/with_history/S1/"+S1+" data/with_history/S1/"+newname)

'''
for S2 in os.listdir("data/S2"):
  S2=S2.split(".")[0]
  date_S2_str=S2.split("_")[1].split("T")[0]
  date_S2=datetime(int(date_S2_str[0:4]),int(date_S2_str[4:6]),int(date_S2_str[6:8]))
  S1s=[]
  for S1 in os.listdir("data/S1"):
    corresponding_S2=S1.split("colwith_")[1].split(".")[0]
    if(corresponding_S2==S2):
      S1s.append(S1)
  if(len(S1s)>1):
    print(S2)
    print(S1s)
    to_be_deleted=[]
    min_days=3
    for S1 in S1s:
      date_str=S1.split("_")[1].split("T")[0]
      date_S1=datetime(int(date_str[0:4]),int(date_str[4:6]),int(date_str[6:8]))
      days_between=date_S2-date_S1
      if(days_between<mind_days):
        min_days=days_between
    for S1 in S1s:
      date_str=S1.split("_")[1].split("T")[0]
      date_S1=datetime(int(date_str[0:4]),int(date_str[4:6]),int(date_str[6:8]))
      days_between=date_S2-date_S1
      if(days_between!=min_days):
        to_be_deleted.append(S1)
    print("To be deleted:")
    print(to_be_deleted)
'''      






