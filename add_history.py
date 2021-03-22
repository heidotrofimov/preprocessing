import os
from PIL import Image
from datetime import datetime

for filename in os.listdir("/home/heido/projects/NDVI_data/merged_tiles_RGB/"):
    print(filename)
    S2_date_str=filename.split("_")[1].split("T")[0]
    S2_date=datetime.strptime(S2_date_str, '%Y%m%d').date()
    tile_nr=filename.split("_")[-2]+"_"+filename.split("_")[-1]
    for filename2 in os.listdir("/home/heido/projects/NDVI_data/S2_RGB_tiles/"):
        history_date_str=filename2.split("_")[1].split("T")[0]
        history_date=datetime.strptime(history_date_str, '%Y%m%d').date()
        
        history_tile_nr=filename2.split("_")[-2]+"_"+filename2.split("_")[-1]
        if(history_date<S2_date and tile_nr==history_tile_nr):
            newname=filename.split("_")[0]+"_"+filename.split("_")[1]+"_"+filename.split("_")[2]+"_"+filename.split("_")[3]+"_"+filename2.split("_")[1]+"_"+tile_nr
            #target=Image.open("/home/heido/projects/NDVI_data/merged_tiles_RGB/"+filename)
            #history=Image.open("/home/heido/projects/NDVI_data/S2_RGB_tiles/"+filename2)
            target=Image.open("/home/heido/projects/NDVI_data/merged_tiles_NDVI/"+filename)
            history=Image.open("/home/heido/projects/NDVI_data/S2_NDVI_tiles/"+filename2)
            dst = Image.new('RGB', (target.width + history.width, target.height))
            dst.paste(target, (0, 0))
            dst.paste(history, (target.width, 0))
            #dst.save("/home/heido/projects/NDVI_data/merged_tiles_NDVI_wh/"+newname)
            dst.save("/home/heido/projects/NDVI_data/merged_tiles_NDVI_wh/"+newname)
            break
