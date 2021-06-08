import os

for filename in os.listdir('collocated'):
  if(".dim" in filename):
    inputfile='collocated/'+filename
    output='collocated_tifs/'+filename.split(".")[0]+'.tif'
    print("/snap/snap8/bin/gpt save_tif.xml -Pinput=\""+inputfile+"\" -Poutput=\""+output+"\"")
