import os
from shutil import copyfile

def S1_name(S1_full):
    S1=S1_full.split("_")
    return S1[0]+"_"+S1[5]+"_"+S1[-1]
  
def S2_name(S2_full):
    S2=S2_full.split("_")
    return S2[0]+"_"+S2[2]+"_"+S2[5]

s1_dict={}

f1=open("full_product_names","r")

lines=f1.readlines()

for line in lines:
  short=line.split(":")[0]
  long=line.split(":")[1].rstrip()
  s1_dict[short]=long
  
f1.close()

for filename in os.listdir("/home/users/biomass/s2_RGB"):
  '''
  s1_part=filename.split("_")[2]+"_"+filename.split("_")[3]
  s1_long=s1_dict[s1_part]
  s1_real=S1_name(s1_long)
  '''
  s2_part=filename.split("_")[0]+"_"+filename.split("_")[1]
  s2_long=s1_dict[s2_part]
  s2_real=S2_name(s2_long).replace(" ","")
  s2_real=s2_real.replace("'","")
  new_name=s2_real+"_"+filename.split("_")[4]+"_"+filename.split("_")[5]
  print(new_name)

 
  #new_name=s1_real+"_colwith_"+s2_real+"_"+filename.split("_")[4]+"_"+filename.split("_")[5]+".tif"
  copyfile("/home/users/biomass/s2_RGB/"+filename,"/home/users/biomass/s2_RGB/"+new_name)
  os.remove("/home/users/biomass/s2_RGB/"+filename)
 
    
    
'''

for filename in os.listdir("/home/users/biomass/s1_files"):
    newname=filename.replace(" ","")
    newname=newname.replace(".tif.tif",".tif")
    newname.replace("'","")
    print(newname)
    copyfile("/home/users/biomass/s1_files/"+filename,"/home/users/biomass/s1_files/"+newname)
    os.remove("/home/users/biomass/s1_files/"+filename)
    
'''
