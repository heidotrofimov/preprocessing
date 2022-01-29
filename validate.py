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

  
  rast_info = rast_open.GetGeoTransform()
  print(rast_info)
  #res_x = rast_info[1]
  #res_y = rast_info[5]
  #print(str(res_x)+" "+str(res_y))
  
