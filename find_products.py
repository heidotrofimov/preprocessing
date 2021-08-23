import os
import numpy as np
import sys
import time
from pathlib import Path
from PIL import Image
sys.path.append('/home/heido/jpy/build/lib.linux-x86_64-3.6')
sys.path.append('/home/heido/.snap/snap-python')
import snappy
from snappy import ProductIO
from snappy import ProductUtils
from snappy import ProgressMonitor
from snappy import Product
from snappy import FlagCoding
from snappy import GPF
from snappy import HashMap
from snappy import ProductData
jpy = snappy.jpy
ImageManager = jpy.get_type('org.esa.snap.core.image.ImageManager')
JAI = jpy.get_type('javax.media.jai.JAI')

Image.MAX_IMAGE_PIXELS = None

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
        product_list.append(product)
    return current_list

def write_rgb_image(bands, filename, format):
    image_info = ProductUtils.createImageInfo(bands, True, ProgressMonitor.NULL)
    im = ImageManager.getInstance().createColoredBandImage(bands, image_info, 0)
    JAI.create("filestore", im, filename, format)

def write_image(band, filename, format):
    im = ImageManager.getInstance().createColoredBandImage([band], band.getImageInfo(), 0)
    JAI.create("filestore", im, filename, format)

def check_data(img):
  img_o=img
  img=img.load()
  for i in range(img_o.width):
    for j in range(img_o.height):
      if(img[i,j][3]==0):
        return False
  return True

def tile_image(im_S2,name,where):
  tiles_x=int(im_S2.width/tile_size)
  tiles_y=int(im_S2.height/tile_size)
  for i in range(0,tiles_x):
    for j in range(0,tiles_y):
      RGB_tile=im_S2.crop((i*tile_size,j*tile_size,tile_size*(i+1),tile_size*(j+1)))
      if(check_data(RGB_tile)):
        where.write(str(i)+"_"+str(j)+"\n")
  if(im_S2.width>tiles_x*tile_size):
    for j in range(0,tiles_y):
      RGB_tile=im_S2.crop((im_S2.width-tile_size,j*tile_size,im_S2.width,tile_size*(j+1)))
      if(check_data(RGB_tile)):
        where.write(str(tiles_x)+"_"+str(j)+"\n")
  if(im_S2.height>tiles_y*tile_size):
    for i in range(0,tiles_x):
      RGB_tile=im_S2.crop((i*tile_size,im_S2.height-tile_size,tile_size*(i+1),im_S2.height))
      if(check_data(RGB_tile)):
        where.write(str(i)+"_"+str(tiles_y)+"\n")
  if(im_S2.height>tiles_y*tile_size and im_S2.width>tiles_x*tile_size):
    RGB_tile=im_S2.crop((im_S2.width-tile_size,im_S2.height-tile_size,im_S2.width,im_S2.height))
    if(check_data(RGB_tile)):
      where.write(str(tiles_x)+"_"+str(tiles_y)+"\n")

def tile_clear_image(im_S2,name,where):
    #Make the mask
    os.system("~/miniconda3/envs/cm_predict/bin/python cm_predict.py -c config/config_example.json -product "+name)
    for filename in os.listdir("prediction/"+name):
        if(".png" in filename):
            mask=Image.open("/home/heido/projects/day_test/prediction/"+name+"/"+filename)
    tiles_x=int(im_S2.width/tile_size)
    tiles_y=int(im_S2.height/tile_size)
    for i in range(0,tiles_x):
        for j in range(0,tiles_y):
            mask_tile=mask.crop((i*tile_size,j*tile_size,tile_size*(i+1),tile_size*(j+1)))
            mask_array=np.array(mask_tile,dtype=np.float)
            if(not any(255 in b for b in mask_array) and not any(192 in b for b in mask_array) and not any(129 in b for b in mask_array)):
                RGB_tile=im_S2.crop((i*tile_size,j*tile_size,tile_size*(i+1),tile_size*(j+1)))
                if(check_data(RGB_tile)):
                    where.write(str(i)+"_"+str(j)+"\n")
    if(im_S2.width>tiles_x*tile_size):
        for j in range(0,tiles_y):
            mask_tile=mask.crop((mask.width-tile_size,j*tile_size,mask.width,tile_size*(j+1)))
            mask_array=np.array(mask_tile,dtype=np.float)
            if(not any(255 in b for b in mask_array) and not any(192 in b for b in mask_array) and not any(129 in b for b in mask_array)):
                RGB_tile=im_S2.crop((im_S2.width-tile_size,j*tile_size,im_S2.width,tile_size*(j+1)))
                if(check_data(RGB_tile)):
                    where.write(str(tiles_x)+"_"+str(j)+"\n")
    if(im_S2.height>tiles_y*tile_size):
        for i in range(0,tiles_x):
            mask_tile=mask.crop((i*tile_size,mask.height-tile_size,tile_size*(i+1),mask.height))
            mask_array=np.array(mask_tile,dtype=np.float)
            if(not any(255 in b for b in mask_array) and not any(192 in b for b in mask_array) and not any(129 in b for b in mask_array)):
                RGB_tile=im_S2.crop((i*tile_size,im_S2.height-tile_size,tile_size*(i+1),im_S2.height))
                if(check_data(RGB_tile)):
                    where.write(str(i)+"_"+str(tiles_y)+"\n")
    if(im_S2.height>tiles_y*tile_size and im_S2.width>tiles_x*tile_size):
        mask_tile=mask.crop((mask.width-tile_size,mask.height-tile_size,mask.width,mask.height))
        mask_array=np.array(mask_tile,dtype=np.float)
        if(not any(255 in b for b in mask_array) and not any(192 in b for b in mask_array) and not any(129 in b for b in mask_array)):
            RGB_tile=im_S2.crop((im_S2.width-tile_size,im_S2.height-tile_size,im_S2.width,im_S2.height))
            if(check_data(RGB_tile)):
                where.write(str(tiles_x)+"_"+str(tiles_y)+"\n")
    os.system("rm -r prediction/*")



year="2019"
place="T34UEA"


os.system("rm month*.xml")
current_dir=place+"_"+year
os.system("mkdir "+current_dir)
os.system("mkdir "+current_dir+"/clear_images")
active_months=["11","10","09","08","07"]

f=open("login.txt","r")
lines=f.readlines()
username=lines[0].rstrip()
password=lines[1].rstrip()
f.close()

product_list=[]

for month in active_months:
    download_xml("S2*MSIL2A*"+year+month+"*"+place+"* AND ( (platformname:Sentinel-2 AND cloudcoverpercentage:[0 TO 4.0])) ","month_"+month+".xml")
    month_list=read_xml("month_"+month+".xml")
    for product in month_list:
        product_list.append(product)

for j in range(len(product_list)):
    month=product_list[j].split("_")[2].split(year)[1][0:2]
    print(month)
    #Download the propduct:
    if(os.path.isfile(current_dir+"/target_images/"+product_list[j]+".txt")==False and os.path.isfile(current_dir+"/clear_images/"+product_list[j]+".txt")==False):
        f=open("products/products.dat","w")
        f.write(product_list[j])
        f.close()
        os.system("~/miniconda3/envs/senpy/bin/python /home/heido/cvat-vsm/dias_old/main_engine.py -d products")
        os.system("mv products/*.SAFE data/")
        #Make the .dim file:
        if(os.path.isdir("data/"+product_list[j]+".SAFE")==True):
            input_path="data/"+product_list[j]+".SAFE/MTD_MSIL2A.xml"
            output_path="data/"+product_list[j]+".SAFE/GRANULE/output.dim"
            line_for_gpt="/snap/snap8/bin/gpt output.xml -Pinput=\""+input_path+"\" -Poutput=\""+output_path+"\""
            os.system(line_for_gpt)
            #Make the RGB image:
            S2_product=ProductIO.readProduct('data/'+product_list[j]+'.SAFE/GRANULE/output.dim')
            band_names = S2_product.getBandNames()
            red = S2_product.getBand('B4')
            green = S2_product.getBand('B3')
            blue = S2_product.getBand('B2')
            write_rgb_image([red, green, blue], product_list[j]+".png", 'png')
            #Tile the image
            im_S2 = Image.open(product_list[j]+".png")
            where1=open(current_dir+"/target_images/"+product_list[j]+".txt","w")
            where2=open(current_dir+"/clear_images/"+product_list[j]+".txt","w")
            #os.system("mkdir target_images/"+product_list[j])
            #os.system("mkdir clear_images/"+product_list[j])
            tile_image(im_S2,product_list[j],where1)
            tile_clear_image(im_S2,product_list[j],where2)
            where1.close()
            where2.close()
            os.system("rm -r data/*")
            os.system("rm -r products/*")
            os.system("rm *.png")
