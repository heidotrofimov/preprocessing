import os
from datetime import datetime, timedelta

days_between=[]
for filename in os.listdir("data/with_history_S2"):
  if("T35VMF" in filename):
    d1s=filename.split("_")[1]
    d2s=filename.split("_")[4]
    d1=datetime(int(d1s[0:4]),int(d1s[4:6]),int(d1s[6:8]))
    d2=datetime(int(d2s[0:4]),int(d2s[4:6]),int(d2s[6:8]))
    bw=abs((d1-d2).days)
    days_between.append(bw)
    
print(days_between)
