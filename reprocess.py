import os
from datetime import datetime


ref_date=datetime(2021,9,6,23,59)

for filename in os.listdir("data/S1"):
  ts=os.path.getmtime("data/S1/"+filename)
  dt=datetime.utcfromtimestamp(ts)
  if(dt>ref_date):
    print(filename)
