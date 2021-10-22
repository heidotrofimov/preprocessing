import os
import sys

'''
AOI="T32UPD"
from="biomass"
to="biomass_test_data"
'''

AOI=sys.argv[1]
fromm=sys.argv[2]
to=sys.argv[3]

for filename in os.listdir(fromm+"/S1/"):
  if(AOI in filename):
    os.system("mv "+fromm+"/S1/"+filename+" "+to+"/S1/")
    
for filename in os.listdir(fromm+"/S2/"):
  if(AOI in filename):
    os.system("mv "+fromm+"/S2/"+filename+" "+to+"/S2/")
    
for filename in os.listdir(fromm+"/S2_RGB/"):
  if(AOI in filename):
    os.system("mv "+fromm+"/S2_RGB/"+filename+" "+to+"/S2_RGB/")
    
    
for filename in os.listdir(fromm+"/with_history/S1/"):
  if(AOI in filename):
    os.system("mv "+fromm+"/with_history/S1/"+filename+" "+to+"/with_history/S1/")
    
for filename in os.listdir(fromm+"/with_history/S2/"):
  if(AOI in filename):
    os.system("mv "+fromm+"/with_history/S2/"+filename+" "+to+"/with_history/S2/")
    
for filename in os.listdir(fromm+"/S2_RGB/"):
  if(AOI in filename):
    os.system("mv "+fromm+"/with_history/S2_RGB/"+filename+" "+to+"/with_history/S2_RGB/")
