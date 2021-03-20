import os

def S2_short(S2):
  return S2.split("_")[5]+"_"+S2.split("_")[2]

for S2 in os.listdir("/home/heido/projects/NDVI_data/S2_RGB_tiles"):
  date=S2.split("_")[0]
  for S2safe in oslistdir("s2_zip"):
    if(S2safe.split("_")[2].split("T")[0]==date):
      S2name=S2_short(S2_safe)
  newname=S2.replace(date,S2name)
  print(S2)
  print(newname)

