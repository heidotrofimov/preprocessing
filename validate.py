import os
import gdal
from gdalconst import GA_ReadOnly

for tiff in os.listdir("/home/users/est_data_with_extra_bands/S1"):
  '''
  im=Image.open("/home/users/est_data_with_extra_bands/S1/"+tiff)
  imarray = np.array(im)
  print(imarray.shape)
  '''
  print(tiff)
  src_ds = gdal.Open("/home/users/est_data_with_extra_bands/S1/"+tiff)
  if src_ds is not None: 
    print ("band count: " + str(src_ds.RasterCount))
