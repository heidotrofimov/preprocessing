import os
from datetime import datetime, timedelta

days_between=[]
target_dates=[]
for filename in os.listdir("data/with_history/S2"):
  if("T35VMF" in filename):
    d1s=filename.split("_")[1]
    if(d1s not in target_dates):
      target_dates.append(d1s)
    d2s=filename.split("_")[4]
    d1=datetime(int(d1s[0:4]),int(d1s[4:6]),int(d1s[6:8]))
    d2=datetime(int(d2s[0:4]),int(d2s[4:6]),int(d2s[6:8]))
    bw=abs((d1-d2).days)
    days_between.append(bw)

    
print(target_dates)    

for target_date in target_dates:
  print(target_date)
  i=0
  for filename in os.listdir("data/with_history/S2"):
    if(target_date in filename):
      i+=1
  print(i)
    

