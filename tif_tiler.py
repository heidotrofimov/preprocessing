"""
    Crop/Subtile S1 Products
    --------
    Subtile into square 512px tiles with overlap at ends to make up for excesses
    (i.e. since tiles from X axis can be 23.35, overlap creates an additional hence 24 images)
"""

import os
from osgeo import gdal

inputPath = "S1B_IW_SLC__1SDV_20200525T042550_20200525T042617_021733_0293FD_F865.tif"
inputTiff = gdal.Open(inputPath)

output_tile_name = "tile"
tile_count = 1
tile_width = 512
tile_height = 512

xOffset = 0
yOffset = 0

xRange = (inputTiff.RasterXSize // tile_width) + 1
yRange = (inputTiff.RasterYSize // tile_height) + 1

images_created = list()
for y_tiles in range(yRange):
    for x_tiles in range(xRange):
        outputPath = f"{output_tile_name}_{tile_count}"
        com_string = "gdal_translate -of GTIFF -srcwin " + str(xOffset)+ ", " + str(yOffset) + ", " + str(tile_width) + ", " + str(tile_height) + " " + str(inputPath) + " " + str(outputPath) + ".tif"
        os.system(com_string)
        
        if inputTiff.RasterXSize - xOffset > 512:
            xOffset += 512
        else:
            xOffset  = inputTiff.RasterXSize - 512
        
        tile_count += 1
    
    xOffset = 0
    
    if inputTiff.RasterYSize - yOffset > 512:
        yOffset += 512
    else:
        yOffset  = inputTiff.RasterYSize - 512 
        

