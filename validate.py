import os
import gdal
from gdalconst import GA_ReadOnly
from libtiff import TIFF

inputdir="collocated_tifs"
for filename in os.listdir(inputdir):
    print(filename)
    inputPath = inputdir+"/"+filename
    inputTiff = gdal.Open(inputPath)
    S1_im=TIFF.open(inputPath)



for tiff in os.listdir("new_data"):
  pass
  '''
  im=Image.open("new_data/"+tiff)
  imarray = np.array(im)
  print(imarray.shape)
  
  #print(tiff)
  src_ds = gdal.Open("new_data/"+tiff)
  x=src_ds.RasterXSize
  y=src_ds.RasterYSize
  result=str(src_ds.RasterCount)+" "+str(x)+" "+str(y)
  if(result!="18 512 512"):
    print(tiff+" "+result)
 
  if("T35VMF" in tiff and "_18_18.tif" in tiff):
    print(tiff)
    src_ds = gdal.Open("/home/users/est_data_with_extra_bands/S1/"+tiff)
    bands=[15,16,17,18]
    for b in bands:
      band = src_ds.GetRasterBand(b)
      arr = band.ReadAsArray()
      print(arr)
  '''
