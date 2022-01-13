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

lines=f.readlines()

for line in lines:
  L2A=line.split(" ")[0]
  tiles=line.split(" ")[1].split(",")
  
  #Otsime L1C
  search=L2A.split("_")[0]+"_"+L2A.split("_")[1].replace("2A","1C")+"_"+L2A.split("_")[2]+"*"+L2A.split("_")[5]+"*"
  download_xml(search,"tmp.xml")
  found=read_xml("tmp.xml")
  print(found)
  
f.close()
