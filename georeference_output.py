import gdal
from gdalconst import GA_ReadOnly
import os
import sys

input_tif=sys.argv[1]  #path to input S1 tif
input_png=sys.argv[2]  #Path to input S2 png. The output PNG will be saved

name_parts=input_png.split("_")
for p in name_parts:
  if(p[0]=="T"):
    EPSG="326"+p[1:2]
print(EPSG)

data = gdal.Open(input_tif, GA_ReadOnly)
geoTransform = data.GetGeoTransform()
minx = geoTransform[0]
maxy = geoTransform[3]
maxx = minx + geoTransform[1] * data.RasterXSize
miny = maxy + geoTransform[5] * data.RasterYSize
print([minx, miny, maxx, maxy])

os.system("gdal_translate -of Gtiff -a_ullr "+str(minx)+" "+str(maxy)+" "+str(maxx)+" "+str(miny)+" -a_srs EPSG:32634 "+input_png+" "+input_png.replace("png","tif"))
