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

jpy = snappy.jpy
ImageManager = jpy.get_type('org.esa.snap.core.image.ImageManager')
JAI = jpy.get_type('javax.media.jai.JAI')

product = ProductIO.readProduct('/home/heido/projects/heido_test/collocated/S1B_IW_GRDH_1SDV_20200504T160332_20200504T160357_021434_028B14_D650.dim')

width = product.getSceneRasterWidth()
height = product.getSceneRasterHeight()

VH = product.getBand('Amplitude_VH_S')
VV = product.getBand('Amplitude_VV_S')

VHVVBand = product.addBand('VHVV', ProductData.TYPE_FLOAT32)
writer = ProductIO.getProductWriter('BEAM-DIMAP')
product.setProductWriter(writer)

rVH = np.zeros(width, dtype=np.float32)
rVV = np.zeros(width, dtype=np.float32)

print("Writing...")

for y in range(height):
    rVH = VH.readPixels(0, y, width, 1, rVH)
    rVV = VV.readPixels(0, y, width, 1, rVV)
    rVHVV = rVH + rVV
    VHVVBand.writePixels(0, y, width, 1, rVHVV)

def write_rgb_image(bands, filename, format):
    image_info = ProductUtils.createImageInfo(bands, True, ProgressMonitor.NULL)
    im = ImageManager.getInstance().createColoredBandImage(bands, image_info, 0)
    JAI.create("filestore", im, filename, format)

red = product.getBand('Amplitude_VH_S')
green = product.getBand('Amplitude_VV_S')
blue = product.getBand('VHVVBand')
write_rgb_image([red, green, blue], 'gamma_export', 'png')

'''
VHVV=product.getBand('VHVV')
rgb=np.zeros((height,width,3))
rgb[...,0]=rVH
rgb[...,1]=rVV
rgb[...,2]=rVH

im_result = Image.fromarray(np.uint8(rgb))
im_result.save("name.png")

w = rad13.getRasterWidth()
h = rad13.getRasterHeight()
rad13_data = np.zeros(w * h, np.float32)
rad13.readPixels(0, 0, w, h, rad13_data)
p.dispose()
rad13_data.shape = h, w
imgplot = plt.imshow(rad13_data)
imgplot.write_png('radiance_13.png')
'''
