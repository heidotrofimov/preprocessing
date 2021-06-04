from PIL import Image
import sys
import os
from shutil import copyfile

tile_size=512

for filename in os.listdir("S2_images"):
  if("NDVI" in filename):
    S2=filename.split("_NDVI")[0]
    condition=False
    for filename2 in os.listdir("s2_RGB_cloudfree"):
      if(S2 in filename2):
        condition=True
        break
    if(condition):
      print(filename)
      im_S2 = Image.open("S2_images/"+filename)
      tiles_x=int(im_S2.width/tile_size)
      tiles_y=int(im_S2.height/tile_size)
      for i in range(0,tiles_x):
        for j in range(0,tiles_y):
          tile="_"+str(i)+"_"+str(j)
          for filename3 in os.listdir("s2_RGB_cloudfree"):
            if(S2 in filename and filename3.split("1SDV")[1].split(".")[0]==tile):
              im_tile_S2=im_S2.crop((i*tile_size,j*tile_size,tile_size*(i+1),tile_size*(j+1)))
              im_tile_S2.save("s2_NDVI_cloudfree/"+filename3)
              break
          
      if(im_S2.width>tiles_x*tile_size):
        for j in range(0,tiles_y):
          tile="_"+str(tiles_x)+"_"+str(j)
          for filename3 in os.listdir("s2_RGB_cloudfree"):
            if(S2 in filename and filename3.split("1SDV")[1].split(".")[0]==tile):
              im_tile_S2=im_S2.crop((im_S2.width-tile_size,j*tile_size,im_S2.width,tile_size*(j+1)))
              im_tile_S2.save("s2_NDVI_cloudfree/"+filename3)
              break
    
      if(im_S2.height>tiles_y*tile_size):
        for i in range(0,tiles_x):
          tile="_"+str(i)+"_"+str(tiles_y)
          for filename3 in os.listdir("s2_RGB_cloudfree"):
            if(S2 in filename and filename3.split("1SDV")[1].split(".")[0]==tile):
              im_tile_S2=im_S2.crop((i*tile_size,im_S2.height-tile_size,tile_size*(i),im_S2.height))
              im_tile_S2.save("s2_NDVI_cloudfree/"+filename3)
              break
          
        if(im_S2.height>tiles_y*tile_size and im_S2.width>tiles_x*tile_size):
          tile="_"+str(tiles_x)+"_"+str(tiles_y)
          for filename3 in os.listdir("s2_RGB_cloudfree"):
            if(S2 in filename and filename3.split("1SDV")[1].split(".")[0]==tile):
              im_tile_S2=im_S2.crop((im_S2.width-tile_size,im_S2.height-tile_size,im_S2.width,im_S2.height))
              im_tile_S2.save("s2_NDVI_cloudfree/"+filename3)
              break
          
