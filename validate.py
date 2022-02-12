import os
import gdal
from gdalconst import GA_ReadOnly

for tiff in os.listdir("/home/users/est_data_with_extra_bands/S1"):
  '''
  im=Image.open("/home/users/est_data_with_extra_bands/S1/"+tiff)
  imarray = np.array(im)
  print(imarray.shape)
  
  #print(tiff)
  src_ds = gdal.Open("new_data/"+tiff)
  x=src_ds.RasterXSize
  y=src_ds.RasterYSize
  result=str(src_ds.RasterCount)+" "+str(x)+" "+str(y)
  if(result!="18 512 512"):
    print(tiff+" "+result)
  '''
  src_ds = gdal.Open("/home/users/est_data_with_extra_bands/S1/"+tiff)
  band = src_ds.GetRasterBand(1)
  arr = band.ReadAsArray()
  print(tiff)
  print(arr)
