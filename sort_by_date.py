import os
import numpy as np
from datetime import datetime, timedelta


#Leiame kõigepealt kõige hilisema


dates=[]
sorted_dates=[]


for product in os.listdir("s2_zip"):
  date_str=product.split("_")[2].split("T")[0]
  dates.append(date_str)
  

while(len(dates)>0):
  referencedate=datetime(2006,10,10)
  date_str1=""
  for date_str in dates:
    date_obj=datetime(int(date_str[0:4]),int(date_str[4:6]),int(date_str[6:8]))
    if(date_obj>referencedate):
      referencedate=date_obj
      date_str1=date_str
  if(date_str1!=""):
    print(date_str1)
    sorted_dates.append(date_str1)
    dates.remove(date_str1)

for i in range(len(sorted_dates)):
  date_str=sorted_dates[i]
  for product in os.listdir("s2_zip"):
    if(date_str in product):
      print(product)
  
      
  
  
