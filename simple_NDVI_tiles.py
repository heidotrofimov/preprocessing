import sys
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import shutil
from datetime import datetime
import argparse
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
   

def S2_short(S2_full):
    S2=S2_full.split(".")[0].split("_")
    return S2[0]+"_"+S2[2]+"_"+S2[5]
    
for S2_SAFE in os.listdir('products'):                   
    NDVI_im=S2_SAFE.split(".")[0]+"_NDVI"
    os.system('mkdir checked_products/'+NDVI_im)
    S2_product=ProductIO.readProduct('products/'+S2_SAFE+'/GRANULE/output.dim')
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
    os.remove('NDVI.dim')
    shutil.rmtree('NDVI.data')
    s2name=S2_short(NDVI_im+".png")
    im_S2 = Image.open(NDVI_im+".png")
    tiles_x=int(im_S2.width/tile_size)
                          
    tiles_y=int(im_S2.height/tile_size)
                          
    for i in range(0,tiles_x):
        for j in range(0,tiles_y):
            rgb="checked_products/"+S2_SAFE.split(".")[0]+"/"+str(i)+"_"+str(j)+".png"
            if(os.path.isfile(rgb)):
                NDVI_tile=im_S2.crop((i*tile_size,j*tile_size,tile_size*(i+1),tile_size*(j+1)))
                NDVI_tile.save('checked_products/'+NDVI_im+"/"+s2name+"_"+str(i)+"_"+str(j)+".png")

    if(im_S2.width>tiles_x*tile_size):
        for j in range(0,tiles_y):
            rgb="checked_products/"+S2_SAFE.split(".")[0]+"/"+str(tiles_x)+"_"+str(j)+".png"
            if(os.path.isfile(rgb)):
                NDVI_tile=im_S2.crop((im_S2.width-tile_size,j*tile_size,im_S2.width,tile_size*(j+1)))
                NDVI_tile.save('checked_products/'+NDVI_im+"/"+s2name+"_"+str(tiles_x)+"_"+str(j)+".png")
    if(im_S2.height>tiles_y*tile_size):
        for i in range(0,tiles_x):
            rgb="checked_products/"+S2_SAFE.split(".")[0]+"/"+str(i)+"_"+str(tiles_y)+".png"
            if(os.path.isfile(rgb)):
                NDVI_tile=im_S2.crop((i*tile_size,im_S2.height-tile_size,tile_size*(i+1),im_S2.height))
                NDVI_tile.save('checked_products/'+NDVI_im+"/"+s2name+"_"+str(i)+"_"+str(tiles_y)+".png")
    if(im_S2.height>tiles_y*tile_size and im_S2.width>tiles_x*tile_size):
        rgb="checked_products/"+S2_SAFE.split(".")[0]+"/"+str(tiles_x)+"_"+str(tiles_y)+".png"
        if(os.path.isfile(rgb)):
            NDVI_tile=im_S2.crop((im_S2.width-tile_size,im_S2.height-tile_size,im_S2.width,im_S2.height))
            NDVI_tile.save('checked_products/'+NDVI_im+"/"+s2name+"_"+str(tiles_x)+"_"+str(tiles_y)+".png")
