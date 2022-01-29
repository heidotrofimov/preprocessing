import os
import gdal
from gdalconst import GA_ReadOnly

for tiff in os.listdir("new_data"):
  '''
  im=Image.open("/home/users/est_data_with_extra_bands/S1/"+tiff)
  imarray = np.array(im)
  print(imarray.shape)
  '''
  #print(tiff)
  src_ds = gdal.Open("new_data/"+tiff)
  print ("band count: " + str(src_ds.RasterCount))
