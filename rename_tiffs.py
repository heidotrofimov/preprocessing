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


for dim in os.listdir('/home/heido/projects/heido_test/s1_iq/'):
  if('.dim' in dim):
    identity=dim.split('.')[0]
    product=ProductIO.readProduct('/home/heido/projects/heido_test/s1_iq/'+dim)
    name=product.getMetadataRoot().getElement('Abstracted_Metadata').getAttribute('PRODUCT').getData()
    os.rename('/home/heido/projects/heido_test/s1_iq/'+identity+'.tif','/home/heido/projects/heido_test/s1_iq/'+name+'.tif')
    
