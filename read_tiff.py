from PIL import Image
import numpy as np
from skimage import io

for tif_file in os.listdir('s1_iq'):
  if('.tif' in tif_file):
    print(tif_file)
    img = io.imread('s1_iq/'+tif_file)
    img = np.asarray(img)
    print(img.dtype)
    print(img.shape)
