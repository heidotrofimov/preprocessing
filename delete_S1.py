import os
from datetime import datetime, timedelta

for S2 in os.listdir("data/S2"):
  S2=S2.split(".")[0]
  S1s=[]
  for S1 in os.listdir("data/S1"):
    corresponding_S2=S1.split("colwith_")[1].split(".")[0]
    if(corresponding_S2==S2):
      S1s.append(S1)
  if(len(S1s)>1):
    print(S2)
    print(S1s)
      






