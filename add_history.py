import os
from PIL import Image
from datetime import datetime, timedelta

for filename in os.listdir("data/S2/"):
    AOI1=filename.split("_")[2]
    date_str1=filename.split("_")[1].split("T")[0]
    date_time_obj1 = datetime(int(date_str1[0:4]),int(date_str1[4:6]),int(date_str1[6:8]))
    tile_nr1=filename.split(AOI1+"_")[1].split(".")[0]
    for filename2 in os.listdir("s2_NDVI/"):
        AOI2=filename2.split("_")[2]
        date_str2=filename2.split("_")[1].split("T")[0]
        date_time_obj2 = datetime(int(date_str2[0:4]),int(date_str2[4:6]),int(date_str2[6:8]))
        tile_nr2=filename2.split(AOI2+"_")[1].split(".")[0]
        if(AOI1==AOI2 and tile_nr1==tile_nr2 and date_time_obj2<date_time_obj1 and (date_time_obj1-date_time_obj2).days<32):
            print(filename+" with "+filename2)
        
