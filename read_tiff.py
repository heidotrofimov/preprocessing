from PIL import Image
import numpy 

im = Image.open('1SDV_8365.tif') 
imarray = numpy.array(im) 
print(imarray.shape)
