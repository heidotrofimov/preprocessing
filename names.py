import os

S2_zip="S2_zip"
S1_zip="/home/heido/projects/heido_test/S1_zip"

def S1_short(S1):
  if("." in S1.split("_")[-1]):
    return S1.split("_"[4])+"_"+S1.split("_")[-1].split(".")[0]
  else:
    return S1.split("_"[4])+"_"+S1.split("_")[-1]
  
def S2_short(S2):
  return S2.split("_")[5]+"_"+S2.split("_")[2]

f = open("full_names.txt","w")

for S2 in os.listdir(S2_zip):
  date=S2.split("_")[2].split("T")[0]
  f.write(S2_short(S2)+": "+S2+"\n")
  for S1 in os.listdir(S1_zip):
    if(S1.split("_")[4].split("T")[0]==date):
      f.write(S1_short(S1)+": "+S1+"\n")
      
f.close()
