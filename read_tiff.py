from PIL import Image
import numpy as np
img = np.asarray(Image.open('1SDV_8365.tif'))
print(img.dtype)
