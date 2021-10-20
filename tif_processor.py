import os
import os.path
from osgeo import gdal
import sys
from libtiff import TIFF
from shutil import copyfile
from datetime import datetime, timedelta
import numpy as np
import time

#Clean before and then copy:
'''
rm -r s1_iq/*
rm -r s1_tif/*
rm -r s1_tif_final/*
rm -r collocated/*
rm -r collocated_tifs/*
mv ../heido_test/s1_iq ./
rm s1_tiles/*
'''

#Use senpy environment for executing this script!

#Rename the tiffs and delete unnecessary tifs before executing this script


#Final output: new files added to s1_tiles

#Tiff linearization:

#Collocation with Sentinel2 products from the same date:

def S1_name(S1_full):
    S1=S1_full.split(".")[0].split("_")
    return S1[0]+"_"+S1[5]+"_"+S1[-2]+"_"+S1[-1]

def S1_name_short(S1_name):
    S1=S1_full.split(".")[0].split("_")
    return S1[0]+"_"+S1[1]+"_"+S1[2]

def S2_name(S2_full):
    S2=S2_full.split(".")[0].split("_")
    return S2[0]+"_"+S2[2]+"_"+S2[5]


f=open("list_for_senpy.txt","r")
nr=f.readlines()
f.close()

count=0

#for n in nr:
for n in nr:
    while(os.path.isfile("senpy_ready.txt")==False):
        time.sleep(300)
        print("Waiting for senpy")
    os.system("rm senpy_ready.txt")
    print("Senpy ready, starting to process!")
    os.system("~/miniconda3/envs/biomass/bin/python rename_tiffs.py")
    os.system("rm -r s1_iq")
        
    os.system("bash linearize_rasters.sh s1_tif")
    os.system("bash combine_tiffs.sh s1_tif")
    os.system("rm s1_tif/*")
    
    
    for S1_tif in os.listdir('s1_tif_final'):
        S1p='s1_tif_final/'+S1_tif
        date1=S1_tif.split("_")[5].split("T")[0]
        date1_o=S1_tif.split("_")[5].split("T")[0]
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
                os.system("/snap/snap8/bin/gpt collocation.xml -PB02=\""+B02+"\" -PS1=\""+S1p+"\" -PB02name=\""+B02name+"\" -Ptargetpath=\""+targetpath+"\"")
                os.system("rm s1_tif_final/"+S1_tif)
        if(found==False):
            date_time_obj = datetime(int(date1_o[0:4]),int(date1_o[4:6]),int(date1_o[6:8]))
            newdate=date_time_obj-timedelta(days=1)
            date1=str(newdate).split()[0].replace("-","")
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
                    os.system("/snap/snap8/bin/gpt collocation.xml -PB02=\""+B02+"\" -PS1=\""+S1p+"\" -PB02name=\""+B02name+"\" -Ptargetpath=\""+targetpath+"\"")
                    os.system("rm s1_tif_final/"+S1_tif)
        if(found==False):
            date_time_obj = datetime(int(date1_o[0:4]),int(date1_o[4:6]),int(date1_o[6:8]))
            newdate=date_time_obj-timedelta(days=2)
            date1=str(newdate).split()[0].replace("-","")
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
                    os.system("/snap/snap8/bin/gpt collocation.xml -PB02=\""+B02+"\" -PS1=\""+S1p+"\" -PB02name=\""+B02name+"\" -Ptargetpath=\""+targetpath+"\"")  
                    os.system("rm s1_tif_final/"+S1_tif)
        if(found==False):
            date_time_obj = datetime(int(date1_o[0:4]),int(date1_o[4:6]),int(date1_o[6:8]))
            newdate=date_time_obj+timedelta(days=1)
            date1=str(newdate).split()[0].replace("-","")
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
                    os.system("/snap/snap8/bin/gpt collocation.xml -PB02=\""+B02+"\" -PS1=\""+S1p+"\" -PB02name=\""+B02name+"\" -Ptargetpath=\""+targetpath+"\"") 
                    os.system("rm s1_tif_final/"+S1_tif)
        if(found==False):
            date_time_obj = datetime(int(date1_o[0:4]),int(date1_o[4:6]),int(date1_o[6:8]))
            newdate=date_time_obj+timedelta(days=2)
            date1=str(newdate).split()[0].replace("-","")
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
                    os.system("/snap/snap8/bin/gpt collocation.xml -PB02=\""+B02+"\" -PS1=\""+S1p+"\" -PB02name=\""+B02name+"\" -Ptargetpath=\""+targetpath+"\"") 
                    os.system("rm s1_tif_final/"+S1_tif)

    os.system("rm s1_tif_final/*")
    #Save the tif files from the collocated data:

    for filename in os.listdir('collocated'):
      if(".dim" in filename):
        inputfile='collocated/'+filename
        output='collocated_tifs/'+filename.split(".")[0]+'.tif'
        os.system("/snap/snap8/bin/gpt save_tif.xml -Pinput=\""+inputfile+"\" -Poutput=\""+output+"\"")
        os.system("rm -r collocated/"+filename.split(".")[0]+"*")
    os.system("rm -r collocated/*")

    #Tile the tif files:
    #Here the "part" part shouldn't matter anymore

    inputdir="collocated_tifs"
    for filename in os.listdir(inputdir):
        print(filename)
        inputPath = inputdir+"/"+filename
        inputTiff = gdal.Open(inputPath)

        S1_im=TIFF.open(inputPath)
        imarray=S1_im.read_image()


        tile_width = 512
        tile_height = 512

        xOffset = 0
        yOffset = 0

        xRange = (inputTiff.RasterXSize // tile_width) + 1
        yRange = (inputTiff.RasterYSize // tile_height) + 1

        images_created = list()
        for y_tiles in range(yRange):
            for x_tiles in range(xRange):
                part1=filename.split("_p")[0]
                part2=filename.split("colwith_")[1]
                name_save=part1+"_colwith_"+part2
                outputPath = "s1_tiles/"+name_save.split(".tif")[0]+"_"+str(x_tiles)+"_"+str(y_tiles)
                corresponding_S2=outputPath.split("colwith_")[1]
                tile_nr=str(x_tiles)+"_"+str(y_tiles)
                s2_tile_exists=False
                for filename2 in os.listdir("s2_NDVI"):
                    if(filename2.split(".")[0]==corresponding_S2):
                        s2_tile_exists=True
                        break



                if(s2_tile_exists==True and os.path.isfile(str(outputPath)+".tif")==False):
                    tifOK=True


                    i=xOffset+10
                    j=yOffset+10
                    if(imarray[0][j][i]==0 or (imarray[1][j][i]==-32768 and imarray[2][j][i]==-32768 and imarray[3][j][i]==-32768 and imarray[4][j][i]==-32768)):
                        tifOK=False
                    if(tifOK==True):

                        datecondition=True    
                        S1_date=filename.split("_")[1].split("T")[0]
                        S1_date_obj=datetime(int(S1_date[0:4]),int(S1_date[4:6]),int(S1_date[6:8]))
                        corresponding_S2=outputPath.split("colwith_")[1]
                        S2_date=corresponding_S2.split("_")[1].split("T")[0]
                        S2_date_obj=datetime(int(S2_date[0:4]),int(S2_date[4:6]),int(S2_date[6:8]))
                        for filename3 in os.listdir("s1_tiles"):
                            if(filename3.split("colwith_")[1].split(".")[0]==corresponding_S2):
                                #If current date is farther away from S2_date than the other date, then we won't proceed
                                other_date=filename3.split("_")[1].split("T")[0]
                                other_date_obj=datetime(int(other_date[0:4]),int(other_date[4:6]),int(other_date[6:8]))
                                if(np.abs((other_date_obj-S2_date_obj).days)<np.abs((S1_date_obj-S2_date_obj).days)):
                                    datecondition=False
                                    break
                        if(datecondition==True):

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

    os.system("rm -r collocated_tifs/*")
    

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
    os.system("~/miniconda3/envs/biomass/bin/python merge.py")
    os.system("rm s1_tiles/*")

    
