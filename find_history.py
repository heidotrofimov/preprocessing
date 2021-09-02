import os
from datetime import datetime, timedelta
AOI=os.listdir("s2_NDVI")[0].split("_")[2]

start_date=datetime(2000,10,10)
end_date=datetime(2030,10,10)
for filename in os.listdir("s2_NDVI"):
  date_str=filename.split("_")[1].split("T")[0]
  date_obj=datetime(int(date_str[0:4]),int(date_str[4:6]),int(date_str[6:8]))
  if(date_obj>start_date):
    start_date=date_obj
  if(date_obj<end_date):
    end_date=date_obj
start_date = start_date - datetime.timedelta(days=1)
end_date = end_date - datetime.timedelta(days=31)
print(start_date)
print(end_date)
