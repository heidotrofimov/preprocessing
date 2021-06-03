from PIL import Image
import numpy as np
from skimage import io
import os
from libtiff import TIFF
import sys


discard=[]

for filename in os.listdir("s1_tiles"):
  path="s1_tiles/"+filename
  S1_im=TIFF.open(path)
  imarray=S1_im.read_image()
  condition=True
  for j in range(len(imarray)):
    for i in range(len(imarray[j])):
      if(imarray[j][i][0]==0):
        condition=False
        if(S1_im not in discard):
          discard.append(S1_im)
        break
    if(condition==False):
      break
        
      
print(len(discard))

