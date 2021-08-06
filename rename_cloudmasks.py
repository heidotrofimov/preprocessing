import os
import shutil

for mask in os.listdir("cloudmasks"):
  date=mask.split("_")[2]
  for product in os.listdir("s2_zip"):
    date2=product.split("_")[2]
    if(date==date2):
      os.mkdir("cloudmasks/"+product.split(".")[0])
      shutil.move("cloudmasks/"+mask,"cloudmasks/"++product.split(".")[0]+"/"+mask)
