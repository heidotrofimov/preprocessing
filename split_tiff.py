#! /usr/bin/python
# coding: utf-8

from osgeo import gdal
from osgeo.gdalconst import *


filename = 'collocated_S1.tif'

# Get the Imagine driver and register it
driver = gdal.GetDriverByName('GTiff')
driver.Register()

dataset = gdal.Open(filename, GA_ReadOnly)
if dataset is None:
    print 'Could not open ' + filename
    sys.exit(1)


cols = dataset.RasterXSize
rows = dataset.RasterYSize
bands = dataset.RasterCount

transform = dataset.GetGeoTransform()
xOrigin = transform[0]
yOrigin = transform[3]
pixelWidth = transform[1]
pixelHeight = transform[5]

for i in range(3):
    x = xValues[i]
    y = yValues[i]

    xOffset = int((x - xOrigin) / pixelWidth)
    yOffset = int((y - yOrigin) / pixelHeight)

    s = str(x) + ' ' + str(y) + ' ' + str(xOffset) + ' ' + str(yOffset) + ' '

    for j in range(bands):
        band = dataset.GetRasterBand(j+1) # 1-based index
        data = band.ReadAsArray(xOffset, yOffset, 1, 1)
        value = data[0,0]
        s = s + str(value) + ' '
print s
