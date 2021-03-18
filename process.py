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
    
    date=product.split("_")[-4]
    
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
        print("processing line ", y, " of ", height)
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
    shutil.move(date+'.png','/home/heido/projects/NDVI_data/S1')

for S2_SAFE in os.listdir('s2'):
    date=S2_SAFE.split("_")[2].split("T")[0]
    S2_product=ProductIO.readProduct('s2/'+S2_SAFE+'/GRANULE/output.dim')
    red = S2_product.getBand('B04')
    green = S2_product.getBand('B03')
    blue = S2_product2.getBand('B02')
    write_rgb_image([red, green, blue], date+'.png', 'png')
    shutil.move(date+'.png','/home/heido/projects/NDVI_data/S2_RGB')
    
    width = S2_product.getSceneRasterWidth()
    height = S2_product.getSceneRasterHeight()
    
    b4 = product.getBand('B04')
    b8 = product.getBand('B08')
    
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
    shutil.move(date+'.png','/home/heido/projects/NDVI_data/S2_NDVI')
    os.remove('NDVI.dim')
    shutil.rmtree('NDVI.data')
