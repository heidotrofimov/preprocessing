import os
from PIL import Image
from datetime import datetime

for filename in os.listdir("/home/heido/projects/NDVI_data/merged_tiles_RGB/"):
    S2_date_str=filename.split("_")[1].split("T")[0]
    S2_date=datetime.strptime(S2_date_str, '%Y%m%d').date()
    print(S2_date)
