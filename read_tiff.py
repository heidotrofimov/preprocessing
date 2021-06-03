from PIL import Image
import numpy as np
from skimage import io
import os
from libtiff import TIFF
import sys

i=0

input=sys.argv[1]

S1_im=TIFF.open(input)
imarray=S1_im.read_image()
print(imarray[0][0][0]==0)

