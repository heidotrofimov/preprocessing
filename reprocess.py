import os
from datetime import datetime


ref_date=datetime(2021,9,6,23,59)

print("Without history:")

products=[]

for filename in os.listdir("data/S1"):
  ts=os.path.getmtime("data/S1/"+filename)
  dt=datetime.utcfromtimestamp(ts)
  if(dt>ref_date):
    products.append(filename)
    
AOIs=[]

for product in products:
  AOI=product.split("_")[-3]
  if(AOI not in AOIs):
    AOIs.append(AOI)
    
for AOI in AOIs:
  dates=[]
  for product in products:
    if(AOI in product):
      S1date_str=product.split("_")[1].split("T")[0]
      if(S1date_str not in dates):
        dates.append(S1date_str)
  print(AOI)
  print(dates)
