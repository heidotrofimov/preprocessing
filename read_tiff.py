from PIL import Image
import numpy as np
img = np.asarray(Image.open('/home/heido/ifg_44_13_9.tif'))
print(img.dtype)
