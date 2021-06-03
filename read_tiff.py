from PIL import Image
import numpy as np
from skimage import io
import os
from libtiff import TIFF

i=0


S1_im=TIFF.open(sys.argv[1])
imarray=S1_im.read_image()
print(imarray)

