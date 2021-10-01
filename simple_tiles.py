import sys
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import shutil
from datetime import datetime
import argparse

for safe in os.listdir("products"):
    if("SAFE" in safe):
        nodim=True
        for filename in os.listdir("products/"+safe+"/GRANULE"):
            if(".dim" in filename):
                nodim=False
        if(nodim):
            input_path="products/"+safe+"/MTD_MSIL2A.xml"
            output_path="products/"+safe+"/GRANULE/output.dim"
            line_for_gpt="/snap/snap8/bin/gpt output.xml -Pinput=\""+input_path+"\" -Poutput=\""+output_path+"\""
            os.system(line_for_gpt)
        
sys.path.append('/home/heido/jpy/build/lib.linux-x86_64-3.6')
sys.path.append('/home/heido/.snap/snap-python')
import snappy
from snappy import ProductIO
from snappy import ProductUtils
from snappy import ProgressMonitor
from snappy import Product
from snappy import FlagCoding
from snappy import GPF
from snappy import HashMap
from snappy import ProductData
jpy = snappy.jpy
ImageManager = jpy.get_type('org.esa.snap.core.image.ImageManager')
JAI = jpy.get_type('javax.media.jai.JAI')

def write_rgb_image(bands, filename, format):
    image_info = ProductUtils.createImageInfo(bands, True, ProgressMonitor.NULL)
    im = ImageManager.getInstance().createColoredBandImage(bands, image_info, 0)
    JAI.create("filestore", im, filename, format)
    
def write_image(band, filename, format):
    im = ImageManager.getInstance().createColoredBandImage([band], band.getImageInfo(), 0)
    JAI.create("filestore", im, filename, format)
    
    
for S2_SAFE in os.listdir('products'):
    RGB_im=S2_SAFE.split(".")[0]
    if(os.path.isfile("products/"+RGB_im+".png")==False):
        S2_product=ProductIO.readProduct('products/'+S2_SAFE+'/GRANULE/output.dim')
        band_names = S2_product.getBandNames()
        red = S2_product.getBand('B4')
        green = S2_product.getBand('B3')
        blue = S2_product.getBand('B2')
        write_rgb_image([red, green, blue], RGB_im+".png", 'png')
        shutil.move(RGB_im+".png",'products/')
        
tile_size=512
AOI="T32UND"

tiles_of_interest=[]

tiles_file=open(AOI+"_tiles_with_fields.txt","r")
lines=tiles_file.readlines()
for line in lines:
    tiles_of_interest.append(line.rstrip())
tiles_file.close()

for RGB_im in os.listdir("products"):
  if(".png" in RGB_im):
      print(RGB_im)
      name=RGB_im.split(".")[0]
      os.mkdir("products/"+name)
      im_S2 = Image.open("products/"+RGB_im)

      tiles_x=int(im_S2.width/tile_size)
      tiles_y=int(im_S2.height/tile_size)
      for i in range(0,tiles_x):
        for j in range(0,tiles_y):
            if(str(i)+"_"+str(j) in tiles_of_interest):
              RGB_tile=im_S2.crop((i*tile_size,j*tile_size,tile_size*(i+1),tile_size*(j+1)))
              RGB_tile.save("products/"+name+"/"+str(i)+"_"+str(j)+".png")
      if(im_S2.width>tiles_x*tile_size):
        for j in range(0,tiles_y):
            if(str(tiles_x)+"_"+str(j) in tiles_of_interest):
              RGB_tile=im_S2.crop((im_S2.width-tile_size,j*tile_size,im_S2.width,tile_size*(j+1)))
              RGB_tile.save("products/"+name+"/"+str(tiles_x)+"_"+str(j)+".png")
      if(im_S2.height>tiles_y*tile_size):
        for i in range(0,tiles_x):
            if(str(i)+"_"+str(tiles_y) in tiles_of_interest):
              RGB_tile=im_S2.crop((i*tile_size,im_S2.height-tile_size,tile_size*(i+1),im_S2.height))
              RGB_tile.save("products/"+name+"/"+str(i)+"_"+str(tiles_y)+".png")
      if(im_S2.height>tiles_y*tile_size and im_S2.width>tiles_x*tile_size):
        if(str(tiles_x)+"_"+str(tiles_y) in tiles_of_interest):
            RGB_tile=im_S2.crop((im_S2.width-tile_size,im_S2.height-tile_size,im_S2.width,im_S2.height))
            RGB_tile.save("products/"+name+"/"+str(tiles_x)+"_"+str(tiles_y)+".png")
