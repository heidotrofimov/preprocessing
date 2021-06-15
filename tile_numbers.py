import os


tiles=[]

for filename in os.listdir("s2_RGB"):
  if("T35VMF" in filename):
    tile=filename.split("T35VMF_")[1].split(".")[0]
    if(tile not in tiles):
      tiles.append(tile)
      
f1=open("T35VMF_tiles_with_fields.txt","w")

for tile in tiles:
  f1.write(tile+"\n")
  
f1.close()
