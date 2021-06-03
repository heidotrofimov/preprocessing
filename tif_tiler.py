"""
    Crop/Subtile S1 Products
    --------
    Subtile into square 512px tiles with overlap at ends to make up for excesses
    (i.e. since tiles from X axis can be 23.35, overlap creates an additional hence 24 images)
"""

import os
from osgeo import gdal
import sys
from libtiff import TIFF
from shutil import copyfile

inputdir="collocated_tifs"
for filename in os.listdir(inputdir):
    print(filename)
    inputPath = inputdir+"/"+filename
    inputTiff = gdal.Open(inputPath)


    tile_width = 512
    tile_height = 512

    xOffset = 0
    yOffset = 0

    xRange = (inputTiff.RasterXSize // tile_width) + 1
    yRange = (inputTiff.RasterYSize // tile_height) + 1

    images_created = list()
    for y_tiles in range(yRange):
        for x_tiles in range(xRange):
            outputPath = "s1_tiles/"+filename.split(".tif")[0]+"_"+str(x_tiles)+"_"+str(y_tiles)
            com_string = "gdal_translate -of GTIFF -srcwin " + str(xOffset)+ ", " + str(yOffset) + ", " + str(tile_width) + ", " + str(tile_height) + " " + str(inputPath) + " " + str(outputPath) + ".tif"
            os.system(com_string)

            if inputTiff.RasterXSize - xOffset > 512:
                xOffset += 512
            else:
                xOffset  = inputTiff.RasterXSize - 512

        xOffset = 0

        if inputTiff.RasterYSize - yOffset > 512:
            yOffset += 512
        else:
            yOffset  = inputTiff.RasterYSize - 512
            
print("cleaning data")

for filename in os.listdir("s1_tiles"):
  print(filename)
  path="s1_tiles/"+filename
  S1_im=TIFF.open(path)
  imarray=S1_im.read_image()
  condition=True
  for j in range(len(imarray)):
    for i in range(len(imarray[j])):
      if(imarray[j][i][0]==0 or (imarray[j][i][1]==-32768 and imarray[j][i][2]==-32768 and imarray[j][i][3]==-32768 and imarray[j][i][4]==-32768)):
        condition=False
        if(path not in discard):
          discard.append(path)
          copyfile(path,'s1_tiles_not/'+filename)
          os.remove(path)
        break
    if(condition==False):
      break

        

