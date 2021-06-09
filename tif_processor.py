import os
from osgeo import gdal
import sys
from libtiff import TIFF
from shutil import copyfile
from datetime import datetime, timedelta

#Use senpy environment for executing this script!

#Rename the tiffs and delete unnecessary tifs before executing this script

#Tiff linearization:

#os.system("bash linearize_rasters.sh s1_tif")
#os.system("bash combine_tiffs.sh s1_tif")

#Collocation with Sentinel2 products from the same date:

def S1_name(S1_full):
    S1=S1_full.split(".")[0].split("_")
    return S1[0]+"_"+S1[4]+"_"+S1[-3]+"_"+S1[-2]+"_"+S1[-1]

def S2_name(S2_full):
    S2=S2_full.split(".")[0].split("_")
    return S2[0]+"_"+S2[2]+"_"+S2[5]

for S1_tif in os.listdir('s1_tif'):
    S1p='s1_tif_final/'+S1_tif
    date1=S1_tif.split("_")[5].split("T")[0]
    print("Original date: "+date1)
    found=False
    for S2_product in os.listdir("s2_zip"):
        date2=S2_product.split("_")[2].split("T")[0]
        if(date1==date2):
            found=True
            name=S1_name(S1_tif)+"_colwith_"+S2_name(S2_product)
            for folder3 in os.listdir('s2_zip/'+S2_product+'/GRANULE/'):
                if("L2" in folder3):
                    for filename in os.listdir('s2_zip/'+S2_product+'/GRANULE/'+folder3+'/IMG_DATA/R10m/'):
                        if('B02_10m.jp2' in filename):
                            B02='/home/heido/projects/preprocessing/s2_zip/'+S2_product+'/GRANULE/'+folder3+'/IMG_DATA/R10m/'+filename
                            B02name=filename
            targetpath='/home/heido/projects/preprocessing/collocated/'+name+".dim"
            #os.system("/snap/snap8/bin/gpt collocation.xml -PB02=\""+B02+"\" -PS1=\""+S1p+"\" -PB02name=\""+B02name+"\" -Ptargetpath=\""+targetpath+"\"")
    if(found==False):
        date_time_obj = datetime(int(date1[0:4]),int(date1[4:6]),int(date1[6:8]))
        newdate=date_time_obj-timedelta(days=1)
        date1=str(newdate)
        print("New date "+date1)
'''
#Save the tif files from the collocated data:

for filename in os.listdir('collocated'):
  if(".dim" in filename):
    inputfile='collocated/'+filename
    output='collocated_tifs/'+filename.split(".")[0]+'.tif'
    os.system("/snap/snap8/bin/gpt save_tif.xml -Pinput=\""+inputfile+"\" -Poutput=\""+output+"\"")
    
#Tile the tif files:

inputdir="collocated_tifs"
for filename in os.listdir(inputdir):
    print(filename)
    inputPath = inputdir+"/"+filename
    inputTiff = gdal.Open(inputPath)


    tile_width = 512
    tile_height = 512

    xOffset = 0
    yOffset = 0

    xRange = (inputTiff.RasterXSize // tile_width) + 1
    yRange = (inputTiff.RasterYSize // tile_height) + 1

    images_created = list()
    for y_tiles in range(yRange):
        for x_tiles in range(xRange):
            outputPath = "s1_tiles/"+filename.split(".tif")[0]+"_"+str(x_tiles)+"_"+str(y_tiles)
            com_string = "gdal_translate -of GTIFF -srcwin " + str(xOffset)+ ", " + str(yOffset) + ", " + str(tile_width) + ", " + str(tile_height) + " " + str(inputPath) + " " + str(outputPath) + ".tif"
            os.system(com_string)

            if inputTiff.RasterXSize - xOffset > 512:
                xOffset += 512
            else:
                xOffset  = inputTiff.RasterXSize - 512

        xOffset = 0

        if inputTiff.RasterYSize - yOffset > 512:
            yOffset += 512
        else:
            yOffset  = inputTiff.RasterYSize - 512
            
#Delete the tif tiles that have regions of no data:

for filename in os.listdir("s1_tiles"):
  print(filename)
  path="s1_tiles/"+filename
  S1_im=TIFF.open(path)
  imarray=S1_im.read_image()
  condition=True
  for j in range(len(imarray)):
    for i in range(len(imarray[j])):
      if(imarray[j][i][0]==0 or (imarray[j][i][1]==-32768 and imarray[j][i][2]==-32768 and imarray[j][i][3]==-32768 and imarray[j][i][4]==-32768)):
        condition=False
        os.remove(path)
        break
    if(condition==False):
      break
'''
