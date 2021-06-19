import os
from PIL import Image
from datetime import datetime, timedelta
from shutil import copyfile

for filename in os.listdir("data/S2/"):
    AOI1=filename.split("_")[2]
    date_str1=filename.split("_")[1].split("T")[0]
    date_time_obj1 = datetime(int(date_str1[0:4]),int(date_str1[4:6]),int(date_str1[6:8]))
    tile_nr1=filename.split(AOI1+"_")[1].split(".")[0]
    list_of_suitables=[]
    max_days=32
    for filename2 in os.listdir("s2_NDVI/"):
        AOI2=filename2.split("_")[2]
        date_str2=filename2.split("_")[1].split("T")[0]
        date_time_obj2 = datetime(int(date_str2[0:4]),int(date_str2[4:6]),int(date_str2[6:8]))
        tile_nr2=filename2.split(AOI2+"_")[1].split(".")[0]
        if(AOI1==AOI2 and tile_nr1==tile_nr2 and date_time_obj2<date_time_obj1 and (date_time_obj1-date_time_obj2).days<max_days):
            found_historical=filename2
            max_days=(date_time_obj1-date_time_obj2).days
    if(max_days<32):
        print(filename+" with "+found_historical)
        S2_filename=filename.split(AOI1)[0]+AOI1+"_"+found_historical.split("_")[0]+"_"+found_historical.split("_")[1]+"_"+tile_nr1+".png"
        target=Image.open("data/S2/"+filename)
        history=Image.open("s2_NDVI/"+found_historical)
        dst = Image.new('RGB', (target.width + history.width, target.height))
        dst.paste(target, (0, 0))
        dst.paste(history, (target.width, 0))
        dst.save("data/with_history/S2/"+S2_filename)
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
            
            
        
