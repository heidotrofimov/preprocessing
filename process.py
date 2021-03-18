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

product2 = ProductIO.readProduct('VHVV.dim')
VHVV= product2.getBand('ndvi')



def write_rgb_image(bands, filename, format):
    image_info = ProductUtils.createImageInfo(bands, True, ProgressMonitor.NULL)
    im = ImageManager.getInstance().createColoredBandImage(bands, image_info, 0)
    JAI.create("filestore", im, filename, format)

red = product.getBand('Amplitude_VH_S')
green = product.getBand('Amplitude_VV_S')
blue = product2.getBand('ndvi')
write_rgb_image([red, green, blue], 'gamma_export', 'png')

