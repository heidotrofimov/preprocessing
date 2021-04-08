from PIL import Image
import numpy 

im = Image.open('s1_iq/combined.tif') 
imarray = numpy.array(im) 
print(imarray.shape)
