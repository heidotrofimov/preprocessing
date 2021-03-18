import os

for S2_product in os.listdir('/home/heido/projects/heido_test/s2_zip'):
  for filename in os.listdir('/home/heido/projects/heido_test/s2_zip/'+S2_product+'/GRANULE/'):
    if("L2" in filename):
      line="/snap/snap8/bin/gpt Write -Ssource=\'/home/heido/projects/heido_test/s2_zip/"+S2_product+"/GRANULE/"+filename+"/\' -Pfile=\'/home/heido/projects/heido_test/s2_zip/"+S2_product+"/GRANULE/"+filename+"/output.dim"
      print(line)
  


