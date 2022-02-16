import os
import os.path
from osgeo import gdal
import sys
from libtiff import TIFF
from shutil import copyfile
from datetime import datetime, timedelta
import numpy as np
import time

for filename in os.listdir("s1_tiles"):
      print(filename)
      path="s1_tiles/"+filename
      S1_im=TIFF.open(path)
      imarray=S1_im.read_image()
      print(imarray[0])
      print(imarray[0].shape)
