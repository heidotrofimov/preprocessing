import os
import time
from pathlib import Path
from PIL import Image, ImageOps
import gdal
from gdalconst import GA_ReadOnly
import os
import sys

tile_size=512

AOIs=["T35VMF","T35VME","T35VMC"]

#AOI="T35VLH"

f=open("../find_products/login.txt","r")
lines=f.readlines()
username=lines[0].rstrip()
password=lines[1].rstrip()
f.close()



def S21(str):
  p=str.split("_")
  return(p[7]+"_MSIL2A*"+p[8].split("T")[0])

def S22(str):
  p=str.split("_")
  return(p[10]+"_MSIL2A*"+p[11].split("T")[0])


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
'''
for AOI in AOIs:
  
  #os.system("rm extra_bands/*")
  #os.system("rm extra_bands_tif/*")

  S2s=[]

  for S1 in os.listdir("/home/users/biomass/extra_historical/S1"):
    AOIc=S1.split("_")[-5]
    if(AOIc==AOI):
      S2_1=S21(S1)+"*"+AOI+"*"
      S2_2=S22(S1)+"*"+AOI+"*"
      if(S2_1 not in S2s):
        S2s.append(S2_1)
      if(S2_2 not in S2s):
        S2s.append(S2_2)

  products=[]  

  for S2 in S2s:
    download_xml(S2,"scihub.xml")
    product=read_xml("scihub.xml")[0]
    products.append(product)
    os.system("rm scihub.xml")

  
  for product in products:
      f=open("products.dat","w")
      f.write(product)
      f.close()
      os.system("python /home/heido/cvat-vsm/dias_download/main_engine.py -d ./")
      os.system("rm products.dat")
      S1s=[]
      tiles=[]
      for S1 in os.listdir("/home/users/biomass/extra_historical/S1"):
        AOIc=S1.split("_")[-5]
        if(AOIc==AOI and ((S1.split("_")[7]==product.split("_")[0] and S1.split("_")[8].split("T")[0]==product.split("_")[2].split("T")[0])  or (S1.split("_")[10]==product.split("_")[0] and S1.split("_")[11].split("T")[0]==product.split("_")[2].split("T")[0])  )):
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



  for png in os.listdir("extra_bands"):
    img=Image.open("extra_bands/"+png)
    new_img=ImageOps.grayscale(img)
    new_img.save("extra_bands/"+png)


EPSG="32635"

for png in os.listdir("extra_bands"):
  input_png="extra_bands/"+png
  print(input_png)
  tile="_"+png.split("_")[-2]+"_"+png.split("_")[-1]
  tile=tile.replace("png","tif")
  input_tif="NOTFOUND"
  for filename in os.listdir("/home/users/biomass/extra_historical/S1"):
    if(AOI in filename and tile in filename):
      input_tif="/home/users/biomass/extra_historical/S1/"+filename
      break
  if(input_tif!="NOTFOUND"):
    data = gdal.Open(input_tif, GA_ReadOnly)
    geoTransform = data.GetGeoTransform()
    minx = geoTransform[0]
    maxy = geoTransform[3]
    maxx = minx + geoTransform[1] * data.RasterXSize
    miny = maxy + geoTransform[5] * data.RasterYSize
    os.system("gdal_translate -of Gtiff -a_ullr "+str(minx)+" "+str(maxy)+" "+str(maxx)+" "+str(miny)+" -a_srs EPSG:"+EPSG+" "+input_png+" extra_bands_tif/"+png.replace("png","tif"))
'''


for AOI in AOIs:
  for tif in os.listdir("/home/users/biomass/extra_historical/S1"):
    if(AOI in tif):
      tile="_"+tif.split("_")[-2]+"_"+tif.split("_")[-1]
      c=tif.split("colwith_")[1].split("_"+AOI)[0].split("_")[1]
      h=tif.split(AOI+"_")[1].split(tile)[0].split("_")[1]
      cb2="NOTFOUND"
      cb3="NOTFOUND"
      cb4="NOTFOUND"
      cb8="NOTFOUND"
      hb2="NOTFOUND"
      hb3="NOTFOUND"
      hb4="NOTFOUND"
      hb8="NOTFOUND"
      for filename in os.listdir("extra_bands_tif"):
        if(tile in filename):
          if(c in filename and "_B2_" in filename):
            cb2="extra_bands_tif/"+filename
          if(c in filename and "_B3_" in filename):
            cb3="extra_bands_tif/"+filename
          if(c in filename and "_B4_" in filename):
            cb4="extra_bands_tif/"+filename
          if(c in filename and "_B8_" in filename):
            cb8="extra_bands_tif/"+filename
          if(h in filename and "_B4_" in filename):
            hb4="extra_bands_tif/"+filename
          if(h in filename and "_B8_" in filename):
            hb8="extra_bands_tif/"+filename  
          if(h in filename and "_B2_" in filename):
            hb2="extra_bands_tif/"+filename  
          if(h in filename and "_B3_" in filename):
            hb3="extra_bands_tif/"+filename  
      print(tif)
      #print("Current b2: "+cb2)
      #print("Current b4: "+cb4)
      #print("Current b8: "+cb8)
      #print("Historical b2: "+hb2)
      #print("Historical b4: "+hb4)
      #print("Historical b8: "+hb8)
      if(hb2!="NOTFOUND"):
        os.system("gdal_merge.py -separate -ot Float32 -of GTiff -o new_data/"+tif+" /home/users/biomass/extra_historical/S1/"+tif+" "+cb2+" "+cb3+" "+cb4+" "+cb8+" "+hb2+" "+hb3+" "+hb4+" "+hb8)


      
      
      
