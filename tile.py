from PIL import Image
import sys
import os

Image.MAX_IMAGE_PIXELS = None

tile_size=512

merged_tiles_RGB="/home/heido/projects/NDVI_data/merged_tiles_RGB"
merged_tiles_NDVI="/home/heido/projects/NDVI_data/merged_tiles_NDVI"
S1_tiles="/home/heido/projects/NDVI_data/S1_tiles"
S2_RGB_tiles="/home/heido/projects/NDVI_data/S2_RGB_tiles"
S2_NDVI_tiles="/home/heido/projects/NDVI_data/S2_NDVI_tiles"

def check_data(img):
  img_o=img
  img=img.load()
  for i in range(img_o.width):
    for j in range(img_o.height):
      if(img[i,j][3]==0):
        return False
  return True

def save(im1,im2,im3,date,tile):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    dst.save(merged_tiles_RGB+"/"+date+"_"+tile+".png")
    dst = Image.new('RGB', (im1.width + im3.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im3, (im1.width, 0))
    dst.save(merged_tiles_NDVI+"/"+date+"_"+tile+".png")
    im1.save(S1_tiles+"/"+date+"_"+tile+".png")
    im2.save(S2_RGB_tiles+"/"+date+"_"+tile+".png")
    im3.save(S2_NDVI_tiles+"/"+date+"_"+tile+".png")

for S2 in os.listdir('/home/heido/projects/NDVI_data/S2_RGB/'):
  date=S2.split(".png")[0]
  for S1 in os.listdir('/home/heido/projects/NDVI_data/S1/'):
    if(S1.split("T")[0]==date):
      print(S2)
      print(S1)
      #Oleme leidnud paari!
      S1='/home/heido/projects/NDVI_data/S1/'+S1
      S2_ndvi='/home/heido/projects/NDVI_data/S2_NDVI/'+S2
      S2='/home/heido/projects/NDVI_data/S2_RGB/'+S2
      S1_im=Image.open(S1)
      S2_im=Image.open(S2)
      S2_NDVI_im=Image.open(S2_ndvi)
      
      tiles_x=int(S1_img.width/tile_size)
      tiles_y=int(S1_img.height/tile_size)
      for i in range(0,tiles_x):
          for j in range(0,tiles_y):
              tile=str(i)+"_"+str(j)
              im_tile_S1=S1_im.crop((i*tile_size,j*tile_size,tile_size*(i+1),tile_size*(j+1)))
              im_tile_S2=S2_im.crop((i*tile_size,j*tile_size,tile_size*(i+1),tile_size*(j+1)))
              im_tile_S2_ndvi=S2_NDVI_im.crop((i*tile_size,j*tile_size,tile_size*(i+1),tile_size*(j+1)))
              if(check_data(im_tile_S1) and check_data(im_tile_S2)):
                  save(im_tile_S1,im_tile_S2,im_tile_S2_ndvi,date,tile)
      if(im_S1.width>tiles_x*tile_size):
          for j in range(0,tiles_y):
              tile=str(tiles_x)+"_"+str(j)
              im_tile_S1=S1_im.crop((S1_im.width-tile_size,j*tile_size,S1_im.width,tile_size*(j+1)))
              im_tile_S2=S2_im.crop((S2_im.width-tile_size,j*tile_size,S2_im.width,tile_size*(j+1)))
              im_tile_S2_ndvi=S2_NDVI_im.crop((S2_NDVI_im.width-tile_size,j*tile_size,S2_NDVI_im.width,tile_size*(j+1)))
              if(check_data(im_tile_S1) and check_data(im_tile_S2)):
                  save(im_tile_S1,im_tile_S2,im_tile_S2_ndvi,date,tile)
      if(im_S1.height>tiles_y*tile_size):
          for i in range(0,tiles_x):
              tile=str(i)+"_"+str(tiles_y)
              im_tile_S1=S1_im.crop((i*tile_size,S1_im.height-tile_size,(i+1)*tile_size,S1_im.height))
              im_tile_S2=S2_im.crop((i*tile_size,S2_im.height-tile_size,(i+1)*tile_size,S2_im.height))
              im_tile_S2_ndvi=S2_NDVI_im.crop((i*tile_size,S2_NDVI_im.height-tile_size,(i+1)*tile_size,S2_NDVI_im.height))
              if(check_data(im_tile_S1) and check_data(im_tile_S2)):
                  save(im_tile_S1,im_tile_S2,im_tile_S2_ndvi,date,tile)
          if(im_S1.width>tiles_x*tile_size):
              tile=str(tiles_x)+"_"+str(tiles_y)
              im_tile_S1=S1_im.crop((S1_im.width-tile_size,S1_im.height-tile_size,S1_im.width,S1_im.height))
              im_tile_S2=S2_im.crop((S2_im.width-tile_size,S2_im.height-tile_size,S2_im.width,S2_im.height))
              im_tile_S2_ndvi=S2_NDVI_im.crop((S2_NDVI_im.width-tile_size,S2_NDVI_im.height-tile_size,S2_NDVI_im.width,S2_NDVI_im.height))
              if(check_data(im_tile_S1) and check_data(im_tile_S2)):
                  save(im_tile_S1,im_tile_S2,im_tile_S2_ndvi,date,tile)
