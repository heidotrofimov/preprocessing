from PIL import Image
import numpy as np
from skimage import io
img = io.imread('/home/heido/ifg_44_13_9.tif')
img = np.asarray(img)
print(img.dtype)
print(img.shape)
