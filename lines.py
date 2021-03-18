import os
import sys

if(sys.argv[1]=="S2"):
  f=open("/home/heido/projects/heido_test/preprocessing/lines_for_gpt.txt","w")
  for S2_product in os.listdir('s2_zip'):
    for filename in os.listdir('s2_zip/'+S2_product+'/GRANULE/'):
      if("L2" in filename):
        if(os.path.exists('s2_zip/'+S2_product+"/GRANULE/output.dim")==False):
          line="/snap/snap8/bin/gpt Write -Ssource=\"s2_zip/"+S2_product+"/GRANULE/"+filename+"/\" -Pfile=\"s2_zip/"+S2_product+"/GRANULE/output.dim\""
          f.write(line+"\n")
        
  f.close()
  


