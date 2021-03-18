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

jpy = snappy.jpy
ImageManager = jpy.get_type('org.esa.snap.core.image.ImageManager')
JAI = jpy.get_type('javax.media.jai.JAI')

product = ProductIO.readProduct('/home/heido/projects/heido_test/collocated/S1B_IW_GRDH_1SDV_20200504T160332_20200504T160357_021434_028B14_D650.dim')

width = product.getSceneRasterWidth()
height = product.getSceneRasterHeight()

VH = product.getBand('Amplitude_VH_S')
VV = product.getBand('Amplitude_VV_S')

###
name = product.getName()
description = product.getDescription()
band_names = product.getBandNames()

newProduct = Product('VHVV', 'VHVV', width, height)
newBand = newProduct.addBand('vhvv', ProductData.TYPE_FLOAT32)
writer = ProductIO.getProductWriter('BEAM-DIMAP')

ProductUtils.copyGeoCoding(product, newProduct)

newProduct.setProductWriter(writer)
newProduct.writeHeader('VHVV.dim')

rVH = numpy.zeros(width, dtype=numpy.float32)
rVV = numpy.zeros(width, dtype=numpy.float32)

for y in range(height2):
    print("processing line ", y, " of ", height)
    rVH = VH.readPixels(0, y, width, 1, rVH)
    rVV = VV.readPixels(0, y, width, 1, rVH)

    VHVV = (rVH + rVV)
    newBand.writePixels(0, y, width, 1, VHVV)

newProduct.closeIO()

###

product2 = ProductIO.readProduct('VHVV.dim')
VHVV= product2.getBand('vhvv')

def write_rgb_image(bands, filename, format):
    image_info = ProductUtils.createImageInfo(bands, True, ProgressMonitor.NULL)
    im = ImageManager.getInstance().createColoredBandImage(bands, image_info, 0)
    JAI.create("filestore", im, filename, format)

red = product.getBand('Amplitude_VH_S')
green = product.getBand('Amplitude_VV_S')
blue = product2.getBand('ndvi')
write_rgb_image([red, green, blue], 'RGB.png', 'png')

