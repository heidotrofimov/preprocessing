import os
import time
from pathlib import Path
from PIL import Image

tile_size=512

'''
f=open("../find_products/login.txt","r")
lines=f.readlines()
username=lines[0].rstrip()
password=lines[1].rstrip()
f.close()

S2s=[]

def S21(str):
  p=str.split("_")
  return(p[7]+"_MSIL2A*"+p[8].split("T")[0])

def S22(str):
  p=str.split("_")
  return(p[10]+"_MSIL2A*"+p[11].split("T")[0])

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
print(len(S2s))
      
def download_xml(product, out_path):
    user_name = username
    user_password = password
    scihub_url = "https://scihub.copernicus.eu/dhus/search?q="
    command = "wget --no-verbose --no-check-certificate --user={user} --password={pwd} --output-document={out}"\
                  " {url}".format(user=user_name, pwd=user_password, out=out_path, url="\""+scihub_url + product+"&rows=100\"")

    #print("Downloading product as " + command)
    os.system(command)
    time.sleep(1.5)  # scihub does not allow too frequent queries; therefore wait a bit before a new query

def read_xml(out_path):
    current_list=[]
    txt = Path(out_path).read_text()
    products=txt.split("<title>")
    for i in range(2,len(products)):
        product=products[i].split("</title>")[0]
        current_list.append(product)
    return current_list

products=[]  

for S2 in S2s:
  download_xml(S2,"scihub.xml")
  product=read_xml("scihub.xml")[0]
  products.append(product)
  os.system("rm scihub.xml")
  
print(products)
print(len(products))
'''
products=['S2B_MSIL2A_20190530T094039_N0212_R036_T35VMF_20190530T123039', 'S2B_MSIL2A_20190517T093039_N0212_R136_T35VMF_20190517T121234', 'S2A_MSIL2A_20190604T094031_N0212_R036_T35VMF_20190604T123219', 'S2A_MSIL2A_20190601T093041_N0212_R136_T35VMF_20190601T114535', 'S2B_MSIL2A_20190616T093039_N0212_R136_T35VMF_20190616T122037', 'S2B_MSIL2A_20190828T094039_N0213_R036_T35VMF_20190828T122001', 'S2B_MSIL2A_20190818T094039_N0213_R036_T35VMF_20190818T123014', 'S2B_MSIL2A_20200819T093039_N0214_R136_T35VMF_20200819T120522', 'S2B_MSIL2A_20200726T095029_N0214_R079_T35VMF_20200726T123818', 'S2B_MSIL2A_20200613T094039_N0214_R036_T35VMF_20200613T123113', 'S2B_MSIL2A_20200531T093039_N0214_R136_T35VMF_20200531T113811', 'S2B_MSIL2A_20200623T094039_N0214_R036_T35VMF_20200623T123518', 'S2A_MSIL2A_20200718T094041_N0214_R036_T35VMF_20200718T111813', 'S2B_MSIL2A_20200809T093039_N0214_R136_T35VMF_20200809T112625', 'S2A_MSIL2A_20200625T093041_N0214_R136_T35VMF_20200625T121318', 'S2A_MSIL2A_20190515T094031_N0212_R036_T35VMF_20190515T111629', 'S2B_MSIL2A_20190729T094039_N0213_R036_T35VMF_20190729T123310', 'S2A_MSIL2A_20200522T095041_N0214_R079_T35VMF_20200522T123919']
i=0
for product in products:
    f=open("products.dat","w")
    f.write(product)
    f.close()
    os.system("python /home/heido/cvat-vsm/dias_old/main_engine.py -d ./")
    os.system("rm products.dat")
    S1s=[]
    tiles=[]
    for S1 in os.listdir("/home/users/biomass/extra_historical/S1"):
      AOI=S1.split("_")[-5]
      if(AOI=="T35VMF" and ((S1.split("_")[7]==product.split("_")[0] and S1.split("_")[8].split("T")[0]==product.split("_")[2].split("T")[0])  or (S1.split("_")[10]==product.split("_")[0] and S1.split("_")[11].split("T")[0]==product.split("_")[2].split("T")[0])  )):
        S1s.append(S1)
        tile=S1.split("_")[-2]+"_"+S1.split("_")[-1].split(".")[0]
        if(tile not in tiles):
          tiles.append(tile)
    tiles_str=""
    for m in tiles:
      tiles_str+=str(m)+","
    os.system("~/miniconda3/envs/biomass/bin/python save_extra_band.py "+product+" "+tiles_str)
    os.system("rm -r "+product+"*")
    os.system("rm *.png")
              

  
