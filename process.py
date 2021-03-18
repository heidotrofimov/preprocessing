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

#Get new band, Vh+VV
GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
BandDescriptor = jpy.get_type('org.esa.snap.core.gpf.common.BandMathsOp$BandDescriptor')

targetBand1 = BandDescriptor()
targetBand1.name = 'VHVV'
targetBand1.type = 'float32'
targetBand1.expression = '(Amplitude_VH_S + Amplitude_VV_S)'

targetBands = jpy.array('org.esa.snap.core.gpf.common.BandMathsOp$BandDescriptor', 2)
targetBands[0] = targetBand1

parameters = HashMap()
parameters.put('targetBands', targetBands)

result = GPF.createProduct('BandMaths', parameters, product)

print("Writing new product")

ProductIO.writeProduct(result, 'snappy_bmaths_output.dim', 'BEAM-DIMAP')


#New band done

'''
def write_rgb_image(bands, filename, format):
    image_info = ProductUtils.createImageInfo(bands, True, ProgressMonitor.NULL)
    im = ImageManager.getInstance().createColoredBandImage(bands, image_info, 0)
    JAI.create("filestore", im, filename, format)

red = product.getBand('Amplitude_VH_S')
green = product.getBand('Amplitude_VV_S')
blue = product.getBand('VHVVBand')
write_rgb_image([red, green, blue], 'gamma_export', 'png')
'''
