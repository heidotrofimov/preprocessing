from PIL import Image
import sys
import os
from shutil import copyfile

def check_data(img):
  img_o=img
  img=img.load()
  for i in range(img_o.width):
    for j in range(img_o.height):
      if(img[i,j][3]==0):
        return False
  return True

Image.MAX_IMAGE_PIXELS = None

tile_size=512

file1 = open('lines_for_gpt.txt', 'r')
file2 = open("full_product_names","w")
lines = file1.readlines()

for line in lines:
  full_S2=line.split("s2_zip/")[1].split(".SAFE")[0]
  full_S1=line.split(".dim")[0].split("collocated_2/")[1]
  S2=line.split("B02name=\"")[1].split("_B02")[0]
  S1=full_S1.split("_")[-1]+"_"+full_S1.split("_")[4]
  file2.write(S2+": "+full_S2+"\n")
  file2.write(S1+": "+full_S1+"\n")
  name=S2+"_"+S1
  for filename in os.listdir("S2_images"):
    if(S2 in filename):
      which=filename.split(".png")[0].split("_")[1]
      im_S2 = Image.open("S2_images/"+filename)
      tiles_x=int(im_S1.width/tile_size)
      tiles_y=int(im_S1.height/tile_size)
      for i in range(0,tiles_x):
        for j in range(0,tiles_y):
          tile="_"+str(i)+"_"+str(j)
          S1_exists=False
          for filename2 in os.listdir("s1_tiles"):
            if(full_S1 in filename2 and tile in filename2):
              S1_exist=True
              break
          if(S1_exist):
            im_tile_S2=im_S2.crop((i*tile_size,j*tile_size,tile_size*(i+1),tile_size*(j+1)))
            if(check_data(im_tile_S2)):
               im_tile_S2.save("s2_"+which+"/"+name+tile+".png")
               if(os.path.isfile("s1_final_tiles/"+name+tile+".tif")==False):
                 copyfile("s1_tiles/"+full_S1+tile+".tif","s1_final_tiles/"+name+tile+".tif")
      if(im_S2.width>tiles_x*tile_size):
        for j in range(0,tiles_y):
          tile="_"+str(tiles_x)+"_"+str(j)
          S1_exists=False
          for filename2 in os.listdir("s1_tiles"):
            if(full_S1 in filename2 and tile in filename2):
              S1_exist=True
              break
          if(S1_exist):
            im_tile_S2=im_S2.crop((im_S2.width-tile_size,j*tile_size,im_S2.width,tile_size*(j+1)))
            if(check_data(im_tile_S2)):
               im_tile_S2.save("s2_"+which+"/"+name+".png")
               if(os.path.isfile("s1_final_tiles/"+name+tile+".tif")==False):
                 copyfile("s1_tiles/"+full_S1+tile+".tif","s1_final_tiles/"+name+tile+".tif")
      if(im_S2.height>tiles_y*tile_size):
        for i in range(0,tiles_x):
          tile="_"+str(i)+"_"+str(tiles_y)
          S1_exists=False
          for filename2 in os.listdir("s1_tiles"):
            if(full_S1 in filename2 and tile in filename2):
              S1_exist=True
              break
          if(S1_exist):
            im_tile_S2=im_S2.crop((i*tile_size,im_S2.height-tile_size,tile_size*(i),im_S2.height))
            if(check_data(im_tile_S2)):
               im_tile_S2.save("s2_"+which+"/"+name+".png")
               if(os.path.isfile("s1_final_tiles/"+name+tile+".tif")==False):
                 copyfile("s1_tiles/"+full_S1+tile+".tif","s1_final_tiles/"+name+tile+".tif")
        if(im_S2.height>tiles_y*tile_size and im_S2.width>tiles_x*tile_size):
          tile="_"+str(tiles_x)+"_"+str(tiles_y)
          S1_exists=False
          for filename2 in os.listdir("s1_tiles"):
            if(full_S1 in filename2 and tile in filename2):
              S1_exist=True
              break
          im_tile_S2=im_S2.crop((im_S2.width-tile_size,im_S2.height-tile_size,im_S2.width,im_S2.height))
          if(check_data(im_tile_S2)):
            im_tile_S2.save("s2_"+which+"/"+name+".png")
            if(os.path.isfile("s1_final_tiles/"+name+tile+".tif")==False):
              copyfile("s1_tiles/"+full_S1+tile+".tif","s1_final_tiles/"+name+tile+".tif")
          
file1.close()
file2.close()

