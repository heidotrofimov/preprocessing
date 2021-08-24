import os
import numpy as np
import sys
import time
from pathlib import Path
from PIL import Image
from datetime import datetime, timedelta
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

list_for_senpy=open("list_for_senpy.txt","w")
tile_size=512
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

def S2_short(S2_full):
    S2=S2_full.split(".")[0].split("_")
    return S2[0]+"_"+S2[2]+"_"+S2[5]

def tile_clear_image(im_S2,name,where):
    AOI=name.split("_")[5]
    tiles_of_interest=[]
    tiles_file=open(AOI+"_tiles_with_fields.txt","r")
    lines=tiles_file.readlines()
    for line in lines:
        tiles_of_interest.append(line.rstrip())
    tiles_file.close()
    #Make the mask
    S2_name=S2_short(name)
    os.system("~/miniconda3/envs/cm_predict/bin/python cm_predict.py -c config/config_example.json --tiling-output prediction_data -product "+name)
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
                if(check_data(RGB_tile) and str(i)+"_"+str(j) in tiles_of_interest):
                    RGB_tile.save(where+"/"+S2_name+"_"+str(i)+"_"+str(j)+".png")
    if(im_S2.width>tiles_x*tile_size):
        for j in range(0,tiles_y):
            mask_tile=mask.crop((mask.width-tile_size,j*tile_size,mask.width,tile_size*(j+1)))
            mask_array=np.array(mask_tile,dtype=np.float)
            if(not any(255 in b for b in mask_array) and not any(192 in b for b in mask_array) and not any(129 in b for b in mask_array)):
                RGB_tile=im_S2.crop((im_S2.width-tile_size,j*tile_size,im_S2.width,tile_size*(j+1)))
                if(check_data(RGB_tile) and str(tiles_x)+"_"+str(j) in tiles_of_interest):
                    RGB_tile.save(where+"/"+S2_name+"_"+str(tiles_x)+"_"+str(j)+".png")
    if(im_S2.height>tiles_y*tile_size):
        for i in range(0,tiles_x):
            mask_tile=mask.crop((i*tile_size,mask.height-tile_size,tile_size*(i+1),mask.height))
            mask_array=np.array(mask_tile,dtype=np.float)
            if(not any(255 in b for b in mask_array) and not any(192 in b for b in mask_array) and not any(129 in b for b in mask_array)):
                RGB_tile=im_S2.crop((i*tile_size,im_S2.height-tile_size,tile_size*(i+1),im_S2.height))
                if(check_data(RGB_tile) and str(i)+"_"+str(tiles_y) in tiles_of_interest):
                    RGB_tile.save(where+"/"+S2_name+"_"+str(i)+"_"+str(tiles_y)+".png")
    if(im_S2.height>tiles_y*tile_size and im_S2.width>tiles_x*tile_size):
        mask_tile=mask.crop((mask.width-tile_size,mask.height-tile_size,mask.width,mask.height))
        mask_array=np.array(mask_tile,dtype=np.float)
        if(not any(255 in b for b in mask_array) and not any(192 in b for b in mask_array) and not any(129 in b for b in mask_array)):
            RGB_tile=im_S2.crop((im_S2.width-tile_size,im_S2.height-tile_size,im_S2.width,im_S2.height))
            if(check_data(RGB_tile) and str(tiles_x)+"_"+str(tiles_y) in tiles_of_interest):
                RGB_tile.save(where+"/"+S2_name+"_"+str(tiles_x)+"_"+str(tiles_y)+".png")
    os.system("rm -r prediction/*")

def tile_NDVI_image(im_S2,name,where,where_RGB):
    S2_name=S2_short(name)
    tiles_x=int(im_S2.width/tile_size)
    tiles_y=int(im_S2.height/tile_size)
    for i in range(0,tiles_x):
        for j in range(0,tiles_y):
            if(os.path.isfile(where_RGB+"/"+S2_name+"_"+str(i)+"_"+str(j)+".png")):
                RGB_tile=im_S2.crop((i*tile_size,j*tile_size,tile_size*(i+1),tile_size*(j+1)))
                RGB_tile.save(where+"/"+S2_name+"_"+str(i)+"_"+str(j)+".png")
    if(im_S2.width>tiles_x*tile_size):
        for j in range(0,tiles_y):
            if(os.path.isfile(where_RGB+"/"+S2_name+"_"+str(tiles_x)+"_"+str(j)+".png")):
                RGB_tile=im_S2.crop((im_S2.width-tile_size,j*tile_size,im_S2.width,tile_size*(j+1)))
                RGB_tile.save(where+"/"+S2_name+"_"+str(tiles_x)+"_"+str(j)+".png")
    if(im_S2.height>tiles_y*tile_size):
        for i in range(0,tiles_x):
            if(os.path.isfile(where_RGB+"/"+S2_name+"_"+str(i)+"_"+str(tiles_y)+".png")):
                RGB_tile=im_S2.crop((i*tile_size,im_S2.height-tile_size,tile_size*(i+1),im_S2.height))
                RGB_tile.save(where+"/"+S2_name+"_"+str(i)+"_"+str(tiles_y)+".png")
    if(im_S2.height>tiles_y*tile_size and im_S2.width>tiles_x*tile_size):
        if(os.path.isfile(where_RGB+"/"+S2_name+"_"+str(tiles_x)+"_"+str(tiles_y)+".png")):
            RGB_tile=im_S2.crop((im_S2.width-tile_size,im_S2.height-tile_size,im_S2.width,im_S2.height))
            RGB_tile.save(where+"/"+S2_name+"_"+str(tiles_x)+"_"+str(tiles_y)+".png")

year="2019"
place="T34UFD"


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
    download_xml("S2*MSIL2A*"+year+month+"*"+place+"* AND ( (platformname:Sentinel-2 AND cloudcoverpercentage:[0 TO 5.0])) ","month_"+month+".xml")
    month_list=read_xml("month_"+month+".xml")
    for product in month_list:
        product_list.append(product)

for j in range(len(product_list)):
    #Download the propduct:
    if(os.path.isdir("prediction_data/"+product_list[j]+".SAFE")==False):
        f=open("prediction_data/products.dat","w")
        f.write(product_list[j])
        f.close()
        os.system("~/miniconda3/envs/senpy/bin/python /home/heido/cvat-vsm/dias_old/main_engine.py -d prediction_data")
        os.system("rm prediction_data/products*")
        #Make the .dim file:
        if(os.path.isdir("prediction_data/"+product_list[j]+".SAFE")==True):
            input_path="prediction_data/"+product_list[j]+".SAFE/MTD_MSIL2A.xml"
            output_path="prediction_data/"+product_list[j]+".SAFE/GRANULE/output.dim"
            line_for_gpt="/snap/snap8/bin/gpt output.xml -Pinput=\""+input_path+"\" -Poutput=\""+output_path+"\""
            os.system(line_for_gpt)
            #Make the RGB image:
            S2_product=ProductIO.readProduct('prediction_data/'+product_list[j]+'.SAFE/GRANULE/output.dim')
            band_names = S2_product.getBandNames()
            red = S2_product.getBand('B4')
            green = S2_product.getBand('B3')
            blue = S2_product.getBand('B2')
            write_rgb_image([red, green, blue], product_list[j]+".png", 'png')
            #Tile the image
            im_S2 = Image.open(product_list[j]+".png")
            os.system("mkdir products/"+product_list[j])
            where="products/"+product_list[j]
            tile_clear_image(im_S2,product_list[j],where)
            os.system("rm "+product_list[j]+".png")
            nr_of_tiles=len([name for name in os.listdir(where) if os.path.isfile(os.path.join(DIR, name))])
            if(nr_of_tiles>75):
                NDVI_im=product_list[j]+"_NDVI"
                width = S2_product.getSceneRasterWidth()
                height = S2_product.getSceneRasterHeight()
                b4 = S2_product.getBand('B4')
                b8 = S2_product.getBand('B8')
                newProduct = Product('NDVI', 'NDVI', width, height)
                newBand = newProduct.addBand('ndvi', ProductData.TYPE_FLOAT32)
                writer = ProductIO.getProductWriter('BEAM-DIMAP')
                ProductUtils.copyGeoCoding(S2_product, newProduct)
                newProduct.setProductWriter(writer)
                newProduct.writeHeader('NDVI.dim')
                rb4 = np.zeros(width, dtype=np.float32)
                rb8 = np.zeros(width, dtype=np.float32)
                for y in range(height):
                    rb4 = b4.readPixels(0, y, width, 1, rb4)
                    rb8 = b8.readPixels(0, y, width, 1, rb8)
                    NDVI = (rb8 - rb4)/(rb8+rb4)
                    newBand.writePixels(0, y, width, 1, NDVI)
                newProduct.closeIO()
                product2 = ProductIO.readProduct('NDVI.dim')
                ndvi_band=product2.getBand('ndvi')
                image_format = 'PNG'
                write_image(ndvi_band, NDVI_im+".png", image_format)
                os.remove('NDVI.dim')
                shutil.rmtree('NDVI.data')
                os.mkdir("products/"+product_list[j]+"_NDVI")
                im_S2_NDVI=Image.open(NDVI_im+".png")
                tile_NDVI_image(im_S2_NDVI,product_list[j],"products/"+product_list[j]+"_NDVI",where)
                os.system("rm "+NDVI_im+".png")
                date_str=product_list[j].split("_")[2].split("T")[0]
                date_obj = datetime(int(date_str[0:4]),int(date_str[4:6]),int(date_str[6:8]))
                date_start=date_obj-timedelta(days=8)
                date_end=date_obj+timedelta(days=2)
                date_start_str=date_start.year+"-"+date_start.month+"-"+date_start.day
                date_end_str=date_end.year+"-"+date_end.month+"-"+date_end.day
                list_for_senpy.write(date_start_str+","+date_end_str+"\n")

list_for_senpy.close()
