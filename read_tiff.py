from PIL import Image
import numpy as np
from skimage import io
import os
from libtiff import TIFF

i=0

for filename in os.listdir('collocated_tifs/'):
  if(i==0):
    S1_im=TIFF.open('collocated_tifs/'+filename)
    imarray=S1_im.read_image()
    print(imarray.dtype)
  i=i+1
