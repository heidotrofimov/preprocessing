import os
from shutil import copyfile

for filename in os.listdir("s1_tiles"):
  new_name=filename.replace(".tif_","_")
  copyfile("s1_tiles/"+filename,"s1_tiles/"+new_name)
  os.remove("s1_tiles/"+filename)
