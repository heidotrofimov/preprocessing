import os
import numpy as np
from PIL import Image

#im_crop = im.crop((left, upper, right, lower))

Image.MAX_IMAGE_PIXELS = None

def crop_up(img):
  img_o=img
  img=img.load()
  pixels_to_be_cropped=[]
  for i in range(img_o.width):
    greatest_from_column=0
    for j in range(img_o.height):
      if(img[i,j][3]==0):
        greatest_from_column=j
      else:
        break
    pixels_to_be_cropped.append(greatest_from_column)
  cropped_img=img_o.crop((0,min(pixels_to_be_cropped),0,0))
  print(min(pixels_to_be_cropped))
  return cropped_img

def crop_bottom(img):
  print(img.width)
  print(img.height)
  img_o=img
  img=img.load()
  pixels_to_be_cropped=[]
  for i in range(img_o.width):
    greatest_from_column=0
    for j in range(img_o.height):
      if(img[img.height-j,i][3]==0):
        greatest_from_column=j
    pixels_to_be_cropped.append(greatest_from_column)
  cropped_img=img_o.crop((0,0,0,min(pixels_to_be_cropped)))
  return cropped_img

def crop_left(img):
  img_o=img
  img=img.load()
  pixels_to_be_cropped=[]
  for i in range(img_o.height):
    greatest_from_row=0
    for j in range(img_o.width):
      if(img[i,j][3]==0):
        greatest_from_row=j
    pixels_to_be_cropped.append(greatest_from_row)
  cropped_img=img_o.crop((min(pixels_to_be_cropped),0,0,0))
  return cropped_img

def crop_right(img):
  img_o=img
  img=img.load()
  pixels_to_be_cropped=[]
  for i in range(img_o.height):
    greatest_from_row=0
    for j in range(img_o.width):
      if(img[i,img.width-j][3]==0):
        greatest_from_row=j
    pixels_to_be_cropped.append(greatest_from_row)
  cropped_img=img_o.crop((0,0,min(pixels_to_be_cropped),0))
  return cropped_img


def first_crop(img):
  img=crop_up(img)
  img=crop_bottom(img)
  img=crop_left(img)
  img=crop_right(img)
  return img
  
for S1 in os.listdir('/home/heido/NDVI_data/big_input_S1_images/'):
  print(S1)
  S1='/home/heido/NDVI_data/big_input_S1_images/'+S1
  S1_img=Image.open(S1)
  S1_cropped=first_crop(S1_img)
  S1_cropped.save('/home/heido/NDVI_data/cropped_examples/'+S1)
  
'''

for S2 in os.listdir('/home/heido/projects/NDVI_data/S2_RGB/'):
  date=S2.split(".png")[0]
  for S1 in os.listdir('/home/heido/projects/NDVI_data/S1/'):
    if(S1.split("T")[0]==date):
      #Oleme leidnud paari!
      S1='/home/heido/projects/NDVI_data/S1/'+S1
      S2='/home/heido/projects/NDVI_data/S2_RGB/'+S2
      S1_img=Image.open(S1)
      S2_img=Image.open(S2)
      S1_cropped=first_crop(S1_img)
      
'''
      
