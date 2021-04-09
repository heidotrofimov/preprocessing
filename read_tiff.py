from PIL import Image
import numpy as np
img = np.asarray(Image.open('S1B_IW_SLC__1SDV_20200525T042524_20200525T042552_021733_0293FD_C565.tif'))
print(img.dtype)
