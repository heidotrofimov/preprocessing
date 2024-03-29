import os
from datetime import datetime


ref_date=datetime(2021,9,6,23,59)
ref_date2=datetime(2021,9,20,23,59)
print("Without history:")

products=[]

i=0
for filename in os.listdir("data/S1"):
  ts=os.path.getmtime("data/S1/"+filename)
  dt=datetime.utcfromtimestamp(ts)
  if(dt>ref_date and dt<ref_date2):
    i=i+1
    print(str(i)+" "+filename+" "+str(dt))
    products.append(filename)
    
AOIs=[]
S2_products=[]

for product in products:
  AOI=product.split("_")[-3]
  S2product=product.split()
  if(AOI not in AOIs):
    AOIs.append(AOI)
    
for AOI in AOIs:
  dates=[]
  for product in products:
    if(AOI in product):
      S1date_str=product.split("_")[1].split("T")[0]
      if(S1date_str not in dates):
        dates.append(S1date_str)
  #print(AOI)
  #print(dates)

print("Test data")  

products=[]
i=0
for filename in os.listdir("test_data/S1"):
  ts=os.path.getmtime("test_data/S1/"+filename)
  dt=datetime.utcfromtimestamp(ts)
  if(dt>ref_date and dt<ref_date2):
    i=i+1
    print(str(i)+" "+filename+" "+str(dt))
    products.append(filename)
'''    
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


print("With history")

products=[]

for filename in os.listdir("data/with_history/S1"):
  ts=os.path.getmtime("data/with_history/S1/"+filename)
  dt=datetime.utcfromtimestamp(ts)
  if(dt>ref_date and dt<ref_date2):
    products.append(filename)
    
AOIs=[]
S2products=[]
for product in products:
  AOI=product.split("_")[-5]
  S2p=product.split("colwith_")[1].split("_S2")[0]
  if(S2p not in S2products):
    S2products.append(S2p)
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
  
print(S2products)

print("Test data")  

products=[]

for filename in os.listdir("test_data/with_history/S1"):
  ts=os.path.getmtime("test_data/with_history/S1/"+filename)
  dt=datetime.utcfromtimestamp(ts)
  if(dt>ref_date and dt<ref_date2):
    products.append(filename)
    
AOIs=[]

for product in products:
  AOI=product.split("_")[-5]
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
'''
