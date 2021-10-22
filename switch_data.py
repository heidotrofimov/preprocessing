import os

'''
AOI="T32UPD"
from="biomass"
to="biomass_test_data"
'''

AOI=sys.argv[1]
from=sys.argv[2]
to=sys.argv[3]

for filename in os.listdir(from+"/S1/"):
  if(AOI in filename):
    os.system("mv "+from+"/S1/"+filename+" "+to+"/S1/")
    
for filename in os.listdir(from+"/S2/"):
  if(AOI in filename):
    os.system("mv "+from+"/S2/"+filename+" "+to+"/S2/")
    
for filename in os.listdir(from+"/S2_RGB/"):
  if(AOI in filename):
    os.system("mv "+from+"/S2_RGB/"+filename+" "+to+"/S2_RGB/")
    
    
for filename in os.listdir(from+"/with_history/S1/"):
  if(AOI in filename):
    os.system("mv "+from+"/with_history/S1/"+filename+" "+to+"/with_history/S1/")
    
for filename in os.listdir(from+"/with_history/S2/"):
  if(AOI in filename):
    os.system("mv "+from+"/with_history/S2/"+filename+" "+to+"/with_history/S2/")
    
for filename in os.listdir(from+"/S2_RGB/"):
  if(AOI in filename):
    os.system("mv "+from+"/with_history/S2_RGB/"+filename+" "+to+"/with_history/S2_RGB/")
