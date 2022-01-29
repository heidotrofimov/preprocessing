import os
from PIL import Image
import numpy as np

for tiff in os.listdir("/home/users/est_data_with_extra_bands"):
  im=Image.open("/home/users/est_data_with_extra_bands/"+tiff)
  imarray = np.array(im)
  print(imarray.shape)
