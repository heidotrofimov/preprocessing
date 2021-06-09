import sys
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import shutil
from datetime import datetime
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--phase", required=True, choices=["full_RGB", "RGB_tiles", "RGB", "NDVI"])
a = parser.parse_args()

for safe in os.listdir("s2_zip"):
    nodim=True
    for filename in os.listdir("s2_zip/"+safe+"/GRANULE"):
        if(".dim" in filename):
            nodim=False
    if(nodim):
        input_path="s2_zip/"+safe+"/MTD_MSIL2A.xml"
        output_path="s2_zip/"+safe+"/GRANULE/output.dim"
        line_for_gpt="/snap/snap8/bin/gpt output.xml -Pinput=\""+input_path+"\" -Poutput=\""+output_path+"\""
        os.system(line_for_gpt)

if(a.phase!="RGB_tiles"):
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

#Biomass environment for this script!

Image.MAX_IMAGE_PIXELS = None

def write_rgb_image(bands, filename, format):
    image_info = ProductUtils.createImageInfo(bands, True, ProgressMonitor.NULL)
    im = ImageManager.getInstance().createColoredBandImage(bands, image_info, 0)
    JAI.create("filestore", im, filename, format)
    
def write_image(band, filename, format):
    im = ImageManager.getInstance().createColoredBandImage([band], band.getImageInfo(), 0)
    JAI.create("filestore", im, filename, format)
    
def S2_short(S2_full):
    S2=S2_full.split(".")[0].split("_")
    return S2[0]+"_"+S2[2]+"_"+S2[5]

def check_data(img):
  img_o=img
  img=img.load()
  for i in range(img_o.width):
    for j in range(img_o.height):
      if(img[i,j][3]==0):
        return False
  return True
  

if(a.phase=="full_RGB" or a.phase=="RGB"):
    for S2_SAFE in os.listdir('s2_zip'):
        RGB_im=S2_SAFE.split(".")[0]
        if(os.path.isfile("S2_images/"+RGB_im+".png")==False):
            S2_product=ProductIO.readProduct('s2_zip/'+S2_SAFE+'/GRANULE/output.dim')
            band_names = S2_product.getBandNames()
            red = S2_product.getBand('B4')
            green = S2_product.getBand('B3')
            blue = S2_product.getBand('B2')
            write_rgb_image([red, green, blue], RGB_im+".png", 'png')
            shutil.move(RGB_im+".png",'S2_images/')
   
   
    
tile_size=512

if(a.phase=="RGB_tiles" or a.phase=="RGB"):
    for RGB_im in os.listdir("S2_images"):
      print(RGB_im)
      name=RGB_im.split(".")[0]
      s2name=S2_short(RGB_im)
      im_S2 = Image.open("S2_images/"+RGB_im)
      for filename in os.listdir("/home/heido/projects/cm_predict/prediction/"+name):
        if(".png" in filename):
          mask=Image.open("/home/heido/projects/cm_predict/prediction/"+name+"/"+filename)
      tiles_x=int(im_S2.width/tile_size)
      tiles_y=int(im_S2.height/tile_size)
      for i in range(0,tiles_x):
        for j in range(0,tiles_y):
          mask_tile=mask.crop((i*tile_size,j*tile_size,tile_size*(i+1),tile_size*(j+1)))
          mask_array=np.array(mask_tile,dtype=np.float)
          if(not any(255 in b for b in mask_array) and not any(192 in b for b in mask_array) and not any(129 in b for b in mask_array)):
              RGB_tile=im_S2.crop((i*tile_size,j*tile_size,tile_size*(i+1),tile_size*(j+1)))
              if(check_data(RGB_tile)):
                RGB_tile.save("s2_RGB/"+s2name+"_"+str(i)+"_"+str(j)+".png")
      if(im_S2.width>tiles_x*tile_size):
        for j in range(0,tiles_y):
          mask_tile=mask.crop((mask.width-tile_size,j*tile_size,mask.width,tile_size*(j+1)))
          mask_array=np.array(mask_tile,dtype=np.float)
          if(not any(255 in b for b in mask_array) and not any(192 in b for b in mask_array) and not any(129 in b for b in mask_array)):
            RGB_tile=im_S2.crop((im_S2.width-tile_size,j*tile_size,im_S2.width,tile_size*(j+1)))
            if(check_data(RGB_tile)):
              RGB_tile.save("s2_RGB/"+s2name+"_"+str(tiles_x)+"_"+str(j)+".png")
      if(im_S2.height>tiles_y*tile_size):
        for i in range(0,tiles_x):
          mask_tile=mask.crop((i*tile_size,mask.height-tile_size,tile_size*(i+1),mask.height))
          mask_array=np.array(mask_tile,dtype=np.float)
          if(not any(255 in b for b in mask_array) and not any(192 in b for b in mask_array) and not any(129 in b for b in mask_array)):
            RGB_tile=im_S2.crop((i*tile_size,im_S2.height-tile_size,tile_size*(i+1),im_S2.height))
            if(check_data(RGB_tile)):
              RGB_tile.save("s2_RGB/"+s2name+"_"+str(i)+"_"+str(tiles_y)+".png")
      if(im_S2.height>tiles_y*tile_size and im_S2.width>tiles_x*tile_size):
        mask_tile=mask.crop((mask.width-tile_size,mask.height-tile_size,mask.width,mask.height))
        mask_array=np.array(mask_tile,dtype=np.float)
        if(not any(255 in b for b in mask_array) and not any(192 in b for b in mask_array) and not any(129 in b for b in mask_array)):
          RGB_tile=im_S2.crop((im_S2.width-tile_size,im_S2.height-tile_size,im_S2.width,im_S2.height))
          if(check_data(RGB_tile)):
            RGB_tile.save("s2_RGB/"+s2name+"_"+str(tiles_x)+"_"+str(tiles_y)+".png")
    
if(a.phase=="NDVI"):
    for S2_SAFE in os.listdir('s2_zip'):
        NDVI_im=S2_SAFE.split(".")[0]+"_NDVI"
        if(os.path.isfile("S2_images/"+NDVI_im+".png")==False):
            S2_product=ProductIO.readProduct('s2_zip/'+S2_SAFE+'/GRANULE/output.dim')
            band_names = S2_product.getBandNames()
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
            write_image(ndvi_band, NDVI_im+".png", image_format)
            shutil.move(NDVI_im+".png",'S2_images')
            os.remove('NDVI.dim')
            shutil.rmtree('NDVI.data')
    for filename in os.listdir("S2_images/"):
        if("NDVI" in filename):
            s2name=S2_short(filename)
            im_S2 = Image.open("S2_images/"+filename)
            tiles_x=int(im_S2.width/tile_size)
            tiles_y=int(im_S2.height/tile_size)
            for i in range(0,tiles_x):
                for j in range(0,tiles_y):
                    rgb="s2_RGB/"+s2name+"_"+str(i)+"_"+str(j)+".png"
                    if(os.path.isfile(rgb)):
                        NDVI_tile=im_S2.crop((i*tile_size,j*tile_size,tile_size*(i+1),tile_size*(j+1)))
                        NDVI_tile.save("s2_NDVI/"+s2name+"_"+str(i)+"_"+str(j)+".png")

            if(im_S2.width>tiles_x*tile_size):
                for j in range(0,tiles_y):
                    rgb="s2_RGB/"+s2name+"_"+str(tiles_x)+"_"+str(j)+".png"
                    if(os.path.isfile(rgb)):
                        NDVI_tile=im_S2.crop((im_S2.width-tile_size,j*tile_size,im_S2.width,tile_size*(j+1)))
                        NDVI_tile.save("s2_NDVI/"+s2name+"_"+str(tiles_x)+"_"+str(j)+".png")
            if(im_S2.height>tiles_y*tile_size):
                for i in range(0,tiles_x):
                    rgb="s2_RGB/"+s2name+"_"+str(i)+"_"+str(tiles_y)+".png"
                    if(os.path.isfile(rgb)):
                        NDVI_tile=im_S2.crop((i*tile_size,im_S2.height-tile_size,tile_size*(i+1),im_S2.height))
                        NDVI_tile.save("s2_NDVI/"+s2name+"_"+str(i)+"_"+str(tiles_y)+".png")
            if(im_S2.height>tiles_y*tile_size and im_S2.width>tiles_x*tile_size):
                rgb="s2_RGB/"+s2name+"_"+str(tiles_x)+"_"+str(tiles_y)+".png"
                if(os.path.isfile(rgb)):
                    NDVI_tile=im_S2.crop((im_S2.width-tile_size,im_S2.height-tile_size,im_S2.width,im_S2.height))
                    NDVI_tile.save("s2_NDVI/"+s2name+"_"+str(tiles_x)+"_"+str(tiles_y)+".png")
