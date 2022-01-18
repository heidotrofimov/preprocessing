import os
import numpy as np
from shutil import copyfile
from PIL import Image
from datetime import datetime, timedelta

#Without history:

s2n=0
s1n=0

for s2 in os.listdir("s2_NDVI"):
  s2_date=s2.split("_")[1].split("T")[0]
  s2_date_obj = datetime(int(s2_date[0:4]),int(s2_date[4:6]),int(s2_date[6:8]))
  days_between=100
  chosen_s1=[]
  for s1 in os.listdir("s1_tiles"):
    if(s1.split("colwith_")[1].split(".")[0]==s2.split(".")[0]):
      s1_date=s1.split("_")[1].split("T")[0]
      s1_date_obj = datetime(int(s1_date[0:4]),int(s1_date[4:6]),int(s1_date[6:8]))
      nr_of_days= np.abs((s2_date_obj-s1_date_obj).days)
      if(nr_of_days<days_between):
        days_between=nr_of_days
  for s1 in os.listdir("s1_tiles"):
    if(s1.split("colwith_")[1].split(".")[0]==s2.split(".")[0]):
      s1_date=s1.split("_")[1].split("T")[0]
      s1_date_obj = datetime(int(s1_date[0:4]),int(s1_date[4:6]),int(s1_date[6:8]))
      nr_of_days=np.abs((s2_date_obj-s1_date_obj).days)
      if(nr_of_days==days_between):
        chosen_s1.append("s1_tiles/"+s1)
  if(len(chosen_s1)!=0):
    s2n=s2n+1
    copyfile("s2_NDVI/"+s2,"data/S2/"+s2)
    try:
      copyfile("s2_RGB/"+s2,"data/S2_RGB/"+s2)
    except:
      pass
    for s1 in chosen_s1:
      copyfile(s1,"data/S1/"+s1.split("/")[1])
      s1n=s1n+1
      
print("Added s1: "+str(s1n))
print("Added s2: "+str(s2n))

s1n=0
s2n=0
       
#Historical images:

for filename in os.listdir("data/S2/"):
    AOI1=filename.split("_")[2]
    date_str1=filename.split("_")[1].split("T")[0]
    date_time_obj1 = datetime(int(date_str1[0:4]),int(date_str1[4:6]),int(date_str1[6:8]))
    tile_nr1=filename.split(AOI1+"_")[1].split(".")[0]
    list_of_suitables=[]
    max_days=25
    for filename2 in os.listdir("s2_NDVI/"):
        AOI2=filename2.split("_")[2]
        date_str2=filename2.split("_")[1].split("T")[0]
        date_time_obj2 = datetime(int(date_str2[0:4]),int(date_str2[4:6]),int(date_str2[6:8]))
        tile_nr2=filename2.split(AOI2+"_")[1].split(".")[0]
        if(AOI1==AOI2 and tile_nr1==tile_nr2 and date_time_obj2<date_time_obj1 and (date_time_obj1-date_time_obj2).days<max_days):
            found_historical=filename2
            max_days=(date_time_obj1-date_time_obj2).days
    if(max_days<32):
        #print(filename+" with "+found_historical)
        S2_filename=filename.split(AOI1)[0]+AOI1+"_"+found_historical.split("_")[0]+"_"+found_historical.split("_")[1]+"_"+tile_nr1+".png"
        if(os.path.isfile("data/with_history/S2/"+S2_filename)==False):
          target=Image.open("data/S2/"+filename)
          history=Image.open("s2_NDVI/"+found_historical)
          dst = Image.new('RGB', (target.width + history.width, target.height))
          dst.paste(target, (0, 0))
          dst.paste(history, (target.width, 0))
          dst.save("data/with_history/S2/"+S2_filename)
          s2n=s2n+1
          try:
            target_RGB=Image.open("data/S2_RGB/"+filename)
            history_RGB=Image.open("s2_RGB/"+found_historical)
            dst_RGB = Image.new('RGB', (target_RGB.width + history_RGB.width, target_RGB.height))
            dst_RGB.paste(target_RGB, (0, 0))
            dst_RGB.paste(history_RGB, (target_RGB.width, 0))
            dst_RGB.save("data/with_history/S2_RGB/"+S2_filename)
          except:
            pass

          for filename3 in os.listdir("data/S1"):
              corresponding_S2=filename3.split("colwith_")[1].replace(".tif",".png")
              if(corresponding_S2==filename):
                  S1_filename=filename3.split("colwith_")[0]+"colwith_"+S2_filename.split(".")[0]+".tif"
                  copyfile("data/S1/"+filename3,"data/with_history/S1/"+S1_filename)
                  s1n=s1n+1
 
print("With historical tiles:")
      
print("Added s1: "+str(s1n))
print("Added s2: "+str(s2n))
    
