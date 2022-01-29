import os
from PIL import Image
import numpy as np

for tiff in os.lsitdir("extra_bands_tif"):
  im=Image.open("extra_bands_tif/"+tiff)
  imarray = numpy.array(im)
  print(imarray.shape)
