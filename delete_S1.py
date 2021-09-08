import os
from datetime import datetime, timedelta
import numpy as np

for S2 in os.listdir("data/with_history/S2"):
  S2=S2.split(".")[0]
  date_S2_str=S2.split("_")[1].split("T")[0]
  date_S2=datetime(int(date_S2_str[0:4]),int(date_S2_str[4:6]),int(date_S2_str[6:8]))
  S1s=[]
  for S1 in os.listdir("data/with_history/S1"):
    corresponding_S2=S1.split("colwith_")[1].split(".")[0]
    if(corresponding_S2==S2):
      S1s.append(S1)
  if(len(S1s)>1):
    #print(S2)
    #print(S1s)
    to_be_deleted=[]
    min_days=3
    for S1 in S1s:
      date_str=S1.split("_")[1].split("T")[0]
      date_S1=datetime(int(date_str[0:4]),int(date_str[4:6]),int(date_str[6:8]))
      days_between=np.abs((date_S2-date_S1).days)
      if(days_between<min_days):
        min_days=days_between
    for S1 in S1s:
      date_str=S1.split("_")[1].split("T")[0]
      date_S1=datetime(int(date_str[0:4]),int(date_str[4:6]),int(date_str[6:8]))
      days_between=np.abs((date_S2-date_S1).days)
      if(days_between!=min_days):
        to_be_deleted.append(S1)
    #print(to_be_deleted)
    for d in to_be_deleted:
      os.system("rm data/with_history/S1/"+d)







