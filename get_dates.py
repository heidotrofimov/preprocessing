import os
import sys

dates=[]

AOI=sys.argv[1]
for filename in os.listdir("data/with_history/S2"):
  if(AOI in filename):
    date=filename.split("_")[1].split("T")[0]
    if(date not in dates):
      dates.append(date)
      
for filename in os.listdir("test_data/with_history/S2"):
  if(AOI in filename):
    date=filename.split("_")[1].split("T")[0]
    if(date not in dates):
      dates.append(date)
      
for date in dates:
  print(date)
    
