import os
from shutil import copyfile

for filename in os.listdir('s2_RGB_cloudfree'):
  for filename2 in os.listdir("s1_final_tiles"):
    if(filename.split(".")[0]==filename.split(".")[0]):
      copyfile("s1_final_tiles/"+filename2,"s1_final_tiles_cloudfree/"+filename2)
      
