from PIL import Image
import numpy as np
from skimage import io
import os

i=0

for filename in os.listdir('collocated_tifs/'):
  if(i==0):
    S1_im=Image.open('collocated_tifs/'+filename)
    imarray=np.array(im)
    print(imarray)
  i=i+1
