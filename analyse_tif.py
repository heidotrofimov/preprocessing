import os
import os.path
from osgeo import gdal
import sys
from libtiff import TIFF
from shutil import copyfile
from datetime import datetime, timedelta
import numpy as np
import time


path="s1_tiles_rejected/S1A_20201126T052448_70E0_colwith_S2A_20201127T102401_T32UPG_13_4.tif"
S1_im=TIFF.open(path)
imarray=S1_im.read_image()
for j in range(len(imarray)):
    print(j)
    for i in range(len(imarray[j])):
      if(imarray[j][i][0]==0 or (imarray[j][i][1]==-32768 and imarray[j][i][2]==-32768 and imarray[j][i][3]==-32768 and imarray[j][i][4]==-32768)):
        print("Alert")

'''
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


for filename in os.listdir("s1_tiles"):
  print(filename)
  path="s1_tiles/"+filename
  S1_im=TIFF.open(path)
  imarray=S1_im.read_image()
  condition=True
  for j in range(len(imarray)):
    for i in range(len(imarray[j])):
      if(imarray[j][i][0]==0):
        print("To be deleted because there's a 0")
        print(str(j)+" "+str(i))
        os.system("mv s1_tiles/"+filename+" to_be_analysed/")
        condition=False
        break
      if(imarray[j][i][1]==-32768 and imarray[j][i][2]==-32768 and imarray[j][i][3]==-32768 and imarray[j][i][4]==-32768):
        print("To be deleted because all are -32768!!!")
        print(str(j)+" "+str(i))
        os.system("mv s1_tiles/"+filename+" to_be_analysed/")
        condition=False
        break
    if(condition==False):
      break
  if(condition==True):
    print("Not to be deleted!")
'''
