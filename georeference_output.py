import gdal
from gdalconst import GA_ReadOnly

data = gdal.Open('data/S1/S1A_20201008T044450_20CC_colwith_S2A_20201006T094041_T34UDA_19_3.tif', GA_ReadOnly)
geoTransform = data.GetGeoTransform()
minx = geoTransform[0]
maxy = geoTransform[3]
maxx = minx + geoTransform[1] * data.RasterXSize
miny = maxy + geoTransform[5] * data.RasterYSize
print [minx, miny, maxx, maxy]
data = None
