import os
import sys

if(sys.argv[1]=="S2"):
  f=open("lines_for_gpt.txt","w")
  for S2_product in os.listdir('/home/heido/projects/heido_test/s2_zip'):
    for filename in os.listdir('/home/heido/projects/heido_test/s2_zip/'+S2_product+'/GRANULE/'):
      if("L2" in filename):
        if(os.path.exists("/home/heido/projects/heido_test/s2_zip/"+S2_product+"/GRANULE/output.dim")==False):
          line="/snap/snap8/bin/gpt Write -Ssource=\'/home/heido/projects/heido_test/s2_zip/"+S2_product+"/GRANULE/"+filename+"/\' -Pfile=\'/home/heido/projects/heido_test/s2_zip/"+S2_product+"/GRANULE/output.dim"
          print(line)
          f.write(line+"\n")
        
  f.close()
  


