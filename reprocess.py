import os
from datetime import datetime


for filename in os.listdir("data/S1"):
  dt=os.path.getmtime("data/S1/"+filename)
  print(datetime.utcfromtimestamp(dt).strftime('%Y-%m-%d %H:%M:%S'))
