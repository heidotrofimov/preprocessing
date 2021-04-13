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

S2_RGB_big_images="final_data/full_S2_RGB"
S2_NDVI_big_images="final_data/full_S2_NDVI"

def S2_short(S2):
  return S2.split("_")[5]+"_"+S2.split("_")[2]
  
#Save the full names

jpy = snappy.jpy
ImageManager = jpy.get_type('org.esa.snap.core.image.ImageManager')
JAI = jpy.get_type('javax.media.jai.JAI')



#Save the full names
S2_zip="s2_zip"
S1_zip="s1_zip"
f = open("full_S2_names.txt","w")
for S2 in os.listdir(S2_zip):
  date=S2.split("_")[2].split("T")[0]
  f.write(S2_short(S2)+": "+S2+"\n")    
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
    
    
