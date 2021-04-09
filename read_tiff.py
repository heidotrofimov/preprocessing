from PIL import Image
import numpy as np
img = np.asarray(Image.open('s1_tif_final/S1A_IW_SLC__1SDV_20200517T044237_20200517T044305_032600_03C696_8FEB.tif'))
print(img.dtype)
