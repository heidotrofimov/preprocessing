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
      os.system("gdal_translate -b 2 -b 3 -b 4 -b 5 s1_tiles/"+filename+" s1_tiles/"+filename)
      print(filename)
      path="s1_tiles/"+filename
      S1_im=TIFF.open(path)
      a=S1_im.read_image()
      if(np.all(a==0)==False and np.all(a==-32768)==False):
            print(a)
