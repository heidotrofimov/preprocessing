import os
import sys
sys.path.append('/home/heido/jpy/build/lib.linux-x86_64-3.6')
sys.path.append('/home/heido/.snap/snap-python')
import snappy
from snappy import ProductIO
import numpy as np
import matplotlib.pyplot as plt
from snappy import ProductData
from PIL import Image
from snappy import ProductUtils
from snappy import ProgressMonitor
from snappy import Product
from snappy import FlagCoding
from snappy import GPF
from snappy import HashMap
from shutil import copyfile
from datetime import datetime

names=[]

for dim in os.listdir('s1_iq/'):
  if('.dim' in dim):
    try:
      identity=dim.split('.')[0]
      product=ProductIO.readProduct('s1_iq/'+dim)
      name=str(product.getMetadataRoot().getElement('Abstracted_Metadata').getAttribute('PRODUCT').getData())
      name2=product.getMetadataRoot().getElement('Slave_Metadata').getElementNames()
      name2=str(name2[0]).split("_Orb")[0]
      date_c_str=name.split("_")[5]
      date_c=datetime(int(date_c_str[0:4]),int(date_c_str[4:6]),int(date_c_str[6:8]))
      date_a_str=name2.split("_")[5]
      date_a=datetime(int(date_a_str[0:4]),int(date_a_str[4:6]),int(date_a_str[6:8]))
      if(date_c>date_a):
          chosen=name
      else:
          chosen=name2
      names.append(chosen)
      k=names.count(chosen)
      chosen=chosen+"_part"+str(k)
      os.rename('/home/heido/projects/preprocessing/s1_iq/'+identity+'.tif','/home/heido/projects/preprocessing/s1_iq/'+chosen+'.tif')
      print(identity+'.tif -> '+chosen+'.tif')
      copyfile('s1_iq/'+chosen+'.tif','s1_tif/'+chosen+'.tif')

    except Exception as e:
      print(str(e))

    
