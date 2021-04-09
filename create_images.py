import sys
sys.path.append('/home/heido/jpy/build/lib.linux-x86_64-3.6')
sys.path.append('/home/heido/.snap/snap-python')
import snappy
from snappy import ProductIO
import numpy as np
import matplotlib.pyplot as plt
from snappy import ProductData
from PIL import Image
from snappy import ProductUtils
from snappy import ProgressMonitor
from snappy import Product
from snappy import FlagCoding
from snappy import GPF
from snappy import HashMap
import os
import shutil
from datetime import datetime


S1_big_images="/home/heido/projects/NDVI_data_2/S1"
S2_RGB_big_images="/home/heido/projects/NDVI_data_2/S2_RGB"
S2_NDVI_big_images="/home/heido/projects/NDVI_data_2/S2_NDVI"

def S2_short(S2):
  return S2.split("_")[5]+"_"+S2.split("_")[2]

def S1_short(S1):
  if("." in S1.split("_")[-1]):
    return S1.split("_")[4]+"_"+S1.split("_")[-1].split(".")[0]
  else:
    return S1.split("_")[4]+"_"+S1.split("_")[-1]
  
#Save the full names


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

for product in os.listdir('/home/heido/projects/preprocessing/collocated/'):
    if(".dim" in product):
        date=S1_short(product)
        product=ProductIO.readProduct('/home/heido/projects/preprocessing/collocated/'+product)
        band_names = product.getBandNames()
        description = product.getDescription()
        print(description)
        



'''
S1_big_images="/home/heido/projects/NDVI_data/S1"
S2_RGB_big_images="/home/heido/projects/NDVI_data/S2_RGB"
S2_NDVI_big_images="/home/heido/projects/NDVI_data/S2_NDVI"

def S2_short(S2):
  return S2.split("_")[5]+"_"+S2.split("_")[2]

def S1_short(S1):
  if("." in S1.split("_")[-1]):
    return S1.split("_")[4]+"_"+S1.split("_")[-1].split(".")[0]
  else:
    return S1.split("_")[4]+"_"+S1.split("_")[-1]
  
#Save the full names

S2_zip="s2_zip"
S1_zip="s1_zip"

f = open("full_names.txt","a")

for S2 in os.listdir(S2_zip):
  date=S2.split("_")[2].split("T")[0]
  f.write(S2_short(S2)+": "+S2+"\n")
  for S1 in os.listdir(S1_zip):
    if(S1.split("_")[4].split("T")[0]==date):
      f.write(S1_short(S1)+": "+S1+"\n")
      
f.close()



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

for product in os.listdir('/home/heido/projects/heido_test/collocated/'):
    if(".dim" in product):
        date=S1_short(product)
        product=ProductIO.readProduct('/home/heido/projects/heido_test/collocated/'+product)
        width = product.getSceneRasterWidth()
        height = product.getSceneRasterHeight()
        VH = product.getBand('Amplitude_VH_S')
        VV = product.getBand('Amplitude_VV_S')
        name = product.getName()
        description = product.getDescription()
        band_names = product.getBandNames()
        newProduct = Product('VHVV', 'VHVV', width, height)
        newBand = newProduct.addBand('vhvv', ProductData.TYPE_FLOAT32)
        writer = ProductIO.getProductWriter('BEAM-DIMAP')
        ProductUtils.copyGeoCoding(product, newProduct)
        newProduct.setProductWriter(writer)
        newProduct.writeHeader('VHVV.dim')
        rVH = np.zeros(width, dtype=np.float32)
        rVV = np.zeros(width, dtype=np.float32)
        for y in range(height):
            rVH = VH.readPixels(0, y, width, 1, rVH)
            rVV = VV.readPixels(0, y, width, 1, rVH)
            VHVV = (rVH + rVV)
            newBand.writePixels(0, y, width, 1, VHVV)
        newProduct.closeIO()
        product2 = ProductIO.readProduct('VHVV.dim')
        red = product.getBand('Amplitude_VH_S')
        green = product.getBand('Amplitude_VV_S')
        blue = product2.getBand('vhvv')
        write_rgb_image([red, green, blue], date+'.png', 'png')
        os.remove('VHVV.dim')
        shutil.rmtree('VHVV.data')
        shutil.move(date+'.png',S1_big_images)

for S2_SAFE in os.listdir('s2_zip'):
    date=S2_short(S2_SAFE)
    S2_product=ProductIO.readProduct('s2_zip/'+S2_SAFE+'/GRANULE/output.dim')
    band_names = S2_product.getBandNames()
    print('s2_zip/'+S2_SAFE+'/GRANULE/output.dim')

    red = S2_product.getBand('B4')
    green = S2_product.getBand('B3')
    blue = S2_product.getBand('B2')
    write_rgb_image([red, green, blue], date+'.png', 'png')
    shutil.move(date+'.png',S2_RGB_big_images)
    
    width = S2_product.getSceneRasterWidth()
    height = S2_product.getSceneRasterHeight()
    
    b4 = S2_product.getBand('B4')
    b8 = S2_product.getBand('B8')
    
    newProduct = Product('NDVI', 'NDVI', width, height)
    newBand = newProduct.addBand('ndvi', ProductData.TYPE_FLOAT32)
    writer = ProductIO.getProductWriter('BEAM-DIMAP')

    ProductUtils.copyGeoCoding(S2_product, newProduct)

    newProduct.setProductWriter(writer)
    newProduct.writeHeader('NDVI.dim')

    rb4 = np.zeros(width, dtype=np.float32)
    rb8 = np.zeros(width, dtype=np.float32)

    for y in range(height):
        rb4 = b4.readPixels(0, y, width, 1, rb4)
        rb8 = b8.readPixels(0, y, width, 1, rb8)
        NDVI = (rb8 - rb4)/(rb8+rb4)
        newBand.writePixels(0, y, width, 1, NDVI)

    newProduct.closeIO()

    product2 = ProductIO.readProduct('NDVI.dim')
    
    ndvi_band=product2.getBand('ndvi')
    image_format = 'PNG'
    write_image(ndvi_band, date+'.png', image_format)
    shutil.move(date+'.png',S2_NDVI_big_images)
    os.remove('NDVI.dim')
    shutil.rmtree('NDVI.data')
    
    
#Tiling:
    
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

def save(im1,im2,im3,date,tile,S1_end):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    dst.save(merged_tiles_RGB+"/"+date+"_"+S1_end+"_"+tile+".png")
    dst = Image.new('RGB', (im1.width + im3.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im3, (im1.width, 0))
    dst.save(merged_tiles_NDVI+"/"+date+"_"+S1_end+"_"+tile+".png")
    im1.save(S1_tiles+"/"+date+"_"+tile+".png")
    im2.save(S2_RGB_tiles+"/"+date+"_"+tile+".png")
    im3.save(S2_NDVI_tiles+"/"+date+"_"+tile+".png")

for S2 in os.listdir(S2_RGB_big_images):
  date=S2.split(".png")[0]
  for filename in os.listdir("merged_tiles_RGB"):
    if(S2 in filename):
      continue
  S2_o=S2
  for S1 in os.listdir(S1_big_images):
    if(S1.split("T")[0]==date):
      S1_end=S1.split(".")[0]
      print(S2)
      print(S1)
      #Oleme leidnud paari!
      S1=S1_big_images+'/'+S1
      S2_ndvi=S2_NDVI_big_images+'/'+S2_o
      S2=S2_RGB_big_images+'/'+S2_o
      S1_im=Image.open(S1)
      S2_im=Image.open(S2)
      S2_NDVI_im=Image.open(S2_ndvi)
      
      tiles_x=int(S1_im.width/tile_size)
      tiles_y=int(S1_im.height/tile_size)
      for i in range(0,tiles_x):
          for j in range(0,tiles_y):
              tile=str(i)+"_"+str(j)
              im_tile_S1=S1_im.crop((i*tile_size,j*tile_size,tile_size*(i+1),tile_size*(j+1)))
              im_tile_S2=S2_im.crop((i*tile_size,j*tile_size,tile_size*(i+1),tile_size*(j+1)))
              im_tile_S2_ndvi=S2_NDVI_im.crop((i*tile_size,j*tile_size,tile_size*(i+1),tile_size*(j+1)))
              if(check_data(im_tile_S1) and check_data(im_tile_S2)):
                  save(im_tile_S1,im_tile_S2,im_tile_S2_ndvi,date,tile,S1_end)
      if(S1_im.width>tiles_x*tile_size):
          for j in range(0,tiles_y):
              tile=str(tiles_x)+"_"+str(j)
              im_tile_S1=S1_im.crop((S1_im.width-tile_size,j*tile_size,S1_im.width,tile_size*(j+1)))
              im_tile_S2=S2_im.crop((S2_im.width-tile_size,j*tile_size,S2_im.width,tile_size*(j+1)))
              im_tile_S2_ndvi=S2_NDVI_im.crop((S2_NDVI_im.width-tile_size,j*tile_size,S2_NDVI_im.width,tile_size*(j+1)))
              if(check_data(im_tile_S1) and check_data(im_tile_S2)):
                  save(im_tile_S1,im_tile_S2,im_tile_S2_ndvi,date,tile,S1_end)
      if(S1_im.height>tiles_y*tile_size):
          for i in range(0,tiles_x):
              tile=str(i)+"_"+str(tiles_y)
              im_tile_S1=S1_im.crop((i*tile_size,S1_im.height-tile_size,(i+1)*tile_size,S1_im.height))
              im_tile_S2=S2_im.crop((i*tile_size,S2_im.height-tile_size,(i+1)*tile_size,S2_im.height))
              im_tile_S2_ndvi=S2_NDVI_im.crop((i*tile_size,S2_NDVI_im.height-tile_size,(i+1)*tile_size,S2_NDVI_im.height))
              if(check_data(im_tile_S1) and check_data(im_tile_S2)):
                  save(im_tile_S1,im_tile_S2,im_tile_S2_ndvi,date,tile,S1_end)
          if(S1_im.width>tiles_x*tile_size):
              tile=str(tiles_x)+"_"+str(tiles_y)
              im_tile_S1=S1_im.crop((S1_im.width-tile_size,S1_im.height-tile_size,S1_im.width,S1_im.height))
              im_tile_S2=S2_im.crop((S2_im.width-tile_size,S2_im.height-tile_size,S2_im.width,S2_im.height))
              im_tile_S2_ndvi=S2_NDVI_im.crop((S2_NDVI_im.width-tile_size,S2_NDVI_im.height-tile_size,S2_NDVI_im.width,S2_NDVI_im.height))
              if(check_data(im_tile_S1) and check_data(im_tile_S2)):
                  save(im_tile_S1,im_tile_S2,im_tile_S2_ndvi,date,tile,S1_end)
'''
