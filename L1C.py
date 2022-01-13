import os
import time
from pathlib import Path

f=open("projects/find_products/login.txt","r")
lines=f.readlines()
username=lines[0].rstrip()
password=lines[1].rstrip()
f.close()

def download_xml(product, out_path):
  user_name = username
  user_password = password
  scihub_url = "https://scihub.copernicus.eu/dhus/search?q="
  command = "wget --no-verbose --no-check-certificate --user={user} --password={pwd} --output-document={out}"\
                " {url}".format(user=user_name, pwd=user_password, out=out_path, url="\""+scihub_url + product+"&rows=100\"")

  print("Downloading product as " + command)
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

f=open("data.txt","r")

f2=open("try_again.txt","w")

lines=f.readlines()

for line in lines:
  L2A=line.split(" ")[0]
  tiles=line.split(" ")[1].split(",")
  
  #Otsime L1C
  search=L2A.split("_")[0]+"_"+L2A.split("_")[1].replace("2A","1C")+"_"+L2A.split("_")[2]+"*"+L2A.split("_")[5]+"*"
  try:
    download_xml(search,"tmp.xml")
    found=read_xml("tmp.xml")
    if(len(found)!=1):
      f2.write(line+"\n")
      continue
    else:
      f3=open("products/products.dat")
      f3.write(found[0])
      f3.close()
      os.system("python cvat-vsm/dias_old/main_engine.py -d products")
      os.system("mkdir L1C_data/"+found[0]+".CVAT")
      for tile in tiles:
        os.system("mkdir L1C_data/"+found[0]+".CVAT/tile_"+tile)
        os.system("mv products/"+found[0]+".CVAT/tile_"+tile+"/*nc L1C_data/"+found[0]+".CVAT/tile_"+tile+"/")
        os.system("mv products/"+found[0]+".CVAT/tile_"+tile+"/*TCI*.png L1C_data/"+found[0]+".CVAT/tile_"+tile+"/")
      os.system("rm -r products/"+found[0]+"*")
  except:
    f2.write(line+"\n")
      
f2.close()
f.close()
