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
  if(str(src_ds.RasterCount)!="18"):
    print(tiff)
    print ("band count: " + str(src_ds.RasterCount))
    
  
  rast_src = "new_data/"+tiff
  rast_open = gdal.Open(rast_src, GA_ReadOnly)
  x=rast_open.RasterXSize
  y=rast_open.RasterYSize
  print(str(x)+" "+str(y))
  
