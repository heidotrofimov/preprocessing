import sys
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import shutil
from datetime import datetime
import argparse

safe=sys.argv[1]+".SAFE"
product=sys.argv[1]
tiles=sys.argv[2].split(",")[0:-1]

print(tiles)

for tile in tiles:
  print(tile)

for filename in os.listdir(safe+"/GRANULE"):
  nodim=True
  if(".dim" in filename):
    nodim=False
  if(nodim):
    input_path=safe+"/MTD_MSIL2A.xml"
    output_path=safe+"/GRANULE/output.dim"
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

tile_size=512

def write_rgb_image(bands, filename, format):
    image_info = ProductUtils.createImageInfo(bands, True, ProgressMonitor.NULL)
    im = ImageManager.getInstance().createColoredBandImage(bands, image_info, 0)
    JAI.create("filestore", im, filename, format)
    
def write_image(band, filename, format):
    im = ImageManager.getInstance().createColoredBandImage([band], band.getImageInfo(), 0)
    JAI.create("filestore", im, filename, format)
 


S2_product=ProductIO.readProduct(safe+'/GRANULE/output.dim')
band_names = S2_product.getBandNames()
red = S2_product.getBand('B4')
NIR = S2_product.getBand('B8')

write_image(red, product+"_B4.png", 'png')
write_image(NIR, product+"_B8.png", 'png')

im_B4 = Image.open(product+"_B4.png")
im_B8 = Image.open(product+"_B8.png")

for tile in tiles:
  print(tile)
  i=int(tile.split("_")[0])
  j=int(tile.split("_")[1])
  if(im_B4.width>i*tile_size and im_B4.height<j*tile_size):
    im_B4_tile=im_B4.crop((im_B4.width-tile_size,j*tile_size,im_B4.width,tile_size*(j+1)))
    im_B8_tile=im_B8.crop((im_B4.width-tile_size,j*tile_size,im_B4.width,tile_size*(j+1)))
  elif(im_B4.height>i*tile_size and im_B4.width<i*tile_size):
    im_B4_tile=im_B4.crop((i*tile_size,im_B4.height-tile_size,tile_size*(i+1),im_B4.height))
    im_B8_tile=im_B8.crop((i*tile_size,im_B4.height-tile_size,tile_size*(i+1),im_B4.height))
  elif(im_B4.width>i*tile_size and im_B4.height>i*tile_size):
    im_B4_tile=im_B4.crop((im_B4.width-tile_size,im_B4.height-tile_size,im_B4.width,im_B4.height))
    im_B8_tile=im_B8.crop((im_B4.width-tile_size,im_B4.height-tile_size,im_B4.width,im_B4.height))
  else:
    im_B4_tile=im_B4.crop((i*tile_size,j*tile_size,tile_size*(i+1),tile_size*(j+1)))
    im_B8_tile=im_B8.crop((i*tile_size,j*tile_size,tile_size*(i+1),tile_size*(j+1)))
  im_B4_tile.save("extra_bands/"+product+"_B4_"+tile+".png")
  im_B8_tile.save("extra_bands/"+product+"_B8_"+tile+".png")
