import os

S2s=[]

def S21(str):
  p=str.split("_")
  return(p[7]+"_MSIL2A*"+p[8].split("T")[0])

def S22(str):
  p=str.split("_")
  return(p[7]+"*"+p[10].split("T")[11])

for S1 in os.listdir("/home/users/biomass/extra_historical/S1"):
  AOI=S1.split("_")[-5]
  if(AOI=="T35VMF"):
    S2_1=S21(S1)+"*T35VMF*"
    S2_2=S22(S1)+"*T35VMF*"
    if(S2_1 not in S2s):
      S2s.append(S2_1)
    if(S2_2 not in S2s):
      S2s.append(S2_2)
      
print(S2s)
