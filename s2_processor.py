import sys
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import shutil
from datetime import datetime

#Biomass environment for this script!

def write_rgb_image(bands, filename, format):
    image_info = ProductUtils.createImageInfo(bands, True, ProgressMonitor.NULL)
    im = ImageManager.getInstance().createColoredBandImage(bands, image_info, 0)
    JAI.create("filestore", im, filename, format)
    
def write_image(band, filename, format):
    im = ImageManager.getInstance().createColoredBandImage([band], band.getImageInfo(), 0)
    JAI.create("filestore", im, filename, format)
    
def S2_short(S2_full):
    S2=S2_full.split(".")[0].split("_")
    return S2[0]+"_"+S2[2]+"_"+S2[5]
  
  
for S2_SAFE in os.listdir('s2_zip'):
    RGB_im=S2_SAFE.split(".")[0]
    if(os.path.isfile("S2_images/"+RGB_im+".png")==False):
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
        S2_product=ProductIO.readProduct('s2_zip/'+S2_SAFE+'/GRANULE/output.dim')
        band_names = S2_product.getBandNames()
        red = S2_product.getBand('B4')
        green = S2_product.getBand('B3')
        blue = S2_product.getBand('B2')
        write_rgb_image([red, green, blue], RGB_im+".png", 'png')
        shutil.move(RGB_im+".png",'S2_images/')
    
tile_size=512
i=0
j=0

for RGB_im in os.listdir("S2_images"):
  name=RGB_im.split(".")[0]
  im_S2 = Image.open("S2_images/"+RGB_im)
  tiles_x=int(im_S2.width/tile_size)
  tiles_y=int(im_S2.height/tile_size)
  for i in range(0,tiles_x):
    for j in range(0,tiles_y):
      tile="_"+str(i)+"_"+str(j)
      #Is this tile cloudfree?
      for tile2 in os.listdir("/home/heido/projects/cm_predict/prediction/"+name):
        if("tile" in tile2):
            tile3=tile2.split("ile")[1]
            if(tile==tile3):
              prediction=Image.open("/home/heido/projects/cm_predict/prediction/"+name+"/"+tile2+"/prediction.png")
              clear=Image.open("/home/heido/projects/cm_predict/prediction/"+name+"/"+tile2+"/predict_CLEAR.png")
              pm=np.array(prediction,dtype=np.float)
              cm=np.array(clear,dtype=np.float)
              if(not any(255 in b for b in pm) and not any(192 in b for b in pm) and not any(129 in b for b in pm)):
                i=i+1
              if(np.all(cm>=200)):
                print(cm)
                j=j+1
                
print(i)
print(j) 
