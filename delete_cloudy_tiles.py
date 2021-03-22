import os
import shutil

f=open("cloudless_tiles.txt","r")

cloudless_tiles=[]

for line in f.readlines():
  cloudless_tiles.append(line.rstrip())
  
for filename in os.listdir("/home/heido/projects/NDVI_data/S2_RGB_tiles"):
  if(filename not in cloudless_tiles):
    os.remove("/home/heido/projects/NDVI_data/S2_RGB_tiles/"+filename)
    
for filename in os.listdir("/home/heido/projects/NDVI_data/S2_NDVI_tiles"):
  if(filename not in cloudless_tiles):
    os.remove("/home/heido/projects/NDVI_data/S2_NDVI_tiles/"+filename)
    
for filename in os.listdir("/home/heido/projects/NDVI_data/merged_tiles_RGB"):
  filename2=filename.split("_")[0]+"_"+filename.split("_")[1]+"_"+filename.split("_")[4]+"_"+filename.split("_")[5]
  if(filename2 not in cloudless_tiles):
    os.remove("/home/heido/projects/NDVI_data/merged_tiles_RGB/"+filename)
    
for filename in os.listdir("/home/heido/projects/NDVI_data/merged_tiles_NDVI"):
  filename2=filename.split("_")[0]+"_"+filename.split("_")[1]+"_"+filename.split("_")[4]+"_"+filename.split("_")[5]
  if(filename2 not in cloudless_tiles):
    os.remove("/home/heido/projects/NDVI_data/merged_tiles_NDVI/"+filename)
