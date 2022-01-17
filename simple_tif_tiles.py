import os
import os.path
from osgeo import gdal
import sys
from libtiff import TIFF
from shutil import copyfile
from datetime import datetime, timedelta
import numpy as np
import time


tile_width=512
tile_height=512
inputPath="S2A_MSIL2A_20210716T095031_N0301_R079_T35VLH_20210716T104451_RGB.tif"

inputTiff = gdal.Open(inputPath)

xOffset = 0
yOffset = 0

xRange = (inputTiff.RasterXSize // tile_width) + 1
yRange = (inputTiff.RasterYSize // tile_height) + 1

for y_tiles in range(yRange):
    for x_tiles in range(xRange):
      outputPath="out/"+str(xOffset)+"_"+str(yOffset)
      com_string = "gdal_translate -of GTIFF -srcwin " + str(xOffset)+ ", " + str(yOffset) + ", " + str(tile_width) + ", " + str(tile_height) + " " + str(inputPath) + " " + str(outputPath) + ".tif"
      if inputTiff.RasterXSize - xOffset > 512:
        xOffset += 512
      else:
        xOffset  = inputTiff.RasterXSize - 512

    xOffset = 0
    if inputTiff.RasterYSize - yOffset > 512:
        yOffset += 512
    else:
        yOffset  = inputTiff.RasterYSize - 512
