from PIL import Image
import numpy as np
from skimage import io
import os
from libtiff import TIFF
import sys

i=0


S1_im=TIFF.open(str(sys.argv[1]))
imarray=S1_im.read_image()
print(imarray)

