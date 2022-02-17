import os
import gdal
from gdalconst import GA_ReadOnly

EPSG="32635"

for s1_tile in os.listdir("s1_tiles_all"):
  print(s1_tile)
  tile="_"+s1_tile.split("_")[-2]+"_"+s1_tile.split("_")[-1].split(".")[0]
  s2=s1_tile.split("colwith_")[1].split(tile)[0]
  p=s2.split("_")
  s2_name=s1_tile.split("colwith_")[1].split(".")[0]
  target_S2=""
  for s2_tile in os.listdir("s2_NDVI"):
    if(s2 in s2_tile and tile in s2_tile):
      target_S2="s2_NDVI/"+s2_tile
      target_RGB="s2_RGB/"+s2_tile
  if(target_S2!=""):
    print("Target: "+target_S2)
    data = gdal.Open("s1_tiles_all/"+s1_tile, GA_ReadOnly)
    geoTransform = data.GetGeoTransform()
    minx = geoTransform[0]
    maxy = geoTransform[3]
    maxx = minx + geoTransform[1] * data.RasterXSize
    miny = maxy + geoTransform[5] * data.RasterYSize
    os.system("gdal_translate -of Gtiff -a_ullr "+str(minx)+" "+str(maxy)+" "+str(maxx)+" "+str(miny)+" -a_srs EPSG:"+EPSG+" "+target_S2+" "+s2_name+".tif")
    os.system("gdal_translate -b 1 "+s2_name+".tif"+" "s2_name+"_new.tif")
    os.system("mv "+s2_name+"_new.tif "+s2_name+".tif")
    #print("gdal_translate -of Gtiff -a_ullr "+str(minx)+" "+str(maxy)+" "+str(maxx)+" "+str(miny)+" -a_srs EPSG:"+EPSG+" "+target_S2+" "+s2_name+".tif")
    NDVI=s2_name+".tif"
    os.system("gdal_translate -of Gtiff -a_ullr "+str(minx)+" "+str(maxy)+" "+str(maxx)+" "+str(miny)+" -a_srs EPSG:"+EPSG+" "+target_RGB+" "+s2_name+"_RGB.tif")
    os.system("gdal_translate -b 1 -b 2 -b 3 "+s2_name+"_RGB.tif"+" "s2_name+"_RGB_new.tif")
    os.system("mv "+s2_name+"_RGB_new.tif "+s2_name+"_RGB.tif")
    #print("gdal_translate -of Gtiff -a_ullr "+str(minx)+" "+str(maxy)+" "+str(maxx)+" "+str(miny)+" -a_srs EPSG:"+EPSG+" "+target_RGB+" "+s2_name+"_RGB.tif")
    RGB=s2_name+"_RGB.tif"
    B8=""
    for dir in os.listdir("b8"):
      if(p[0] in dir and p[1] in dir and p[2] in dir):
        for filename in os.listdir("b8/"+dir):
          if(tile in filename):
            B8="b8/"+dir+"/"+filename
    if(B8!=""):
      os.system("gdal_translate -of Gtiff -a_ullr "+str(minx)+" "+str(maxy)+" "+str(maxx)+" "+str(miny)+" -a_srs EPSG:"+EPSG+" "+B8+" "+s2_name+"_B8.tif")
      os.system("gdal_translate -b 1 "+s2_name+"_B8.tif"+" "s2_name+"_B8_new.tif")
      os.system("mv "+s2_name+"_B8_new.tif "+s2_name+"_B8.tif")
      #print("gdal_translate -of Gtiff -a_ullr "+str(minx)+" "+str(maxy)+" "+str(maxx)+" "+str(miny)+" -a_srs EPSG:"+EPSG+" "+B8+" "+s2_name+"_B8.tif")
      B8t=s2_name+"_B8.tif"
      os.system("gdal_merge.py -separate -ot Float32 -of GTiff -o T35VLH_data/"+s1_tile+" s1_tiles_all/"+s1_tile+" "+NDVI+" "+RGB+" "+B8t)
      #print("gdal_merge.py -separate -ot Float32 -of GTiff -o T35VLH_data/"+s1_tile+" s1_tiles_all/"+s1_tile+" "+NDVI+" "+RGB+" "+B8t)
      os.system("rm "+NDVI)
      os.system("rm "+RGB)
      os.system("rm "+B8t)
  else:
    print("No target found")
