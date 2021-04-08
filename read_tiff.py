from PIL import Image
import numpy 

im = Image.open('s1_iq/combined.tiff') 
imarray = numpy.array(im) 
print(imarray.shape)
