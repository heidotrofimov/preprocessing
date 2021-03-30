import os
from PIL import Image

for filename in os.listdir('/home/heido/projects/NDVI_data/S2_RGB_tiles/'):
  for filename2 in os.listdir('/home/heido/projects/NDVI_data/S2_NDVI_tiles/'):
    if(filename==filename2):
      RGB=Image.open("/home/heido/projects/NDVI_data/S2_RGB_tiles/"+filename)
      NDVI=Image.open("/home/heido/projects/NDVI_data/S2_NDVI_tiles/"+filename2)
      dst = Image.new('RGB', (RGB.width + NDVI.width, RGB.height))
      dst.paste(RGB, (0, 0))
      dst.paste(NDVI, (RGB.width, 0))
      dst.save("/home/heido/projects/NDVI_data/RGB_NDVI/"+filename)
    
