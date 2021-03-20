import os

def S2_short(S2):
  return S2.split("_")[5]+"_"+S2.split("_")[2]

def S1_short(S1):
  if("." in S1.split("_")[-1]):
    return S1.split("_")[4]+"_"+S1.split("_")[-1].split(".")[0]
  else:
    return S1.split("_")[4]+"_"+S1.split("_")[-1]

'''
for S2 in os.listdir("/home/heido/projects/NDVI_data/S2_RGB_tiles"):
  date=S2.split("_")[0]
  for S2safe in os.listdir("s2_zip"):
    if(S2safe.split("_")[2].split("T")[0]==date):
      S2name=S2_short(S2safe)
  newname=S2.replace(date,S2name)
  os.rename("/home/heido/projects/NDVI_data/S2_RGB_tiles/"+S2,"/home/heido/projects/NDVI_data/S2_RGB_tiles/"+newname)
  os.rename("/home/heido/projects/NDVI_data/S2_NDVI_tiles/"+S2,"/home/heido/projects/NDVI_data/S2_NDVI_tiles/"+newname)
  '''

for merged in os.listdir("/home/heido/projects/NDVI_data/merged_tiles_RGB"):
  S1date=merged.split("_")[0]+"T"+merged.split("_")[1].split(".")[0]
  print(S1date)
  date=merged.split("_")[0]
  tile=merged.split("_")[-2]+"_"+merged.split("_")[-1].split(".")[0]
  for S1file in os.listdir("/home/heido/projects/heido_test/s1_zip"):
    if(S1file.split("_")[4]==S1date):
      S1name=S1_short(S1file)
  for S2safe in os.listdir("s2_zip"):
    if(S2safe.split("_")[2].split("T")[0]==date):
      S2name=S2_short(S2safe)
  newname=S2name+"_"+S1name+"_"+tile+".png"
  print(merged)
  print(newname)
    
    
      
      
    


