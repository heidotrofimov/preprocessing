import os

for filename in os.listdir('collocated_2'):
  if(".dim" in filename):
    inputfile='collocated_2/'+filename
    output='collocated_tifs/'+filename+'.tif'
    print("/snap/snap8/bin/gpt save_tif.xml -Pinput=\""+inputfile+"\" -Poutput=\""+output+"\"")
