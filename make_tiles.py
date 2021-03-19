from PIL import Image
import sys
import os

Image.MAX_IMAGE_PIXELS = None

tile_size=512

from_where='sentinel_data/sentinel_images_cropped_and_merged/'
from_where='sentinel_data/example/'
where_to='sentinel_data/tiles_512/'


def identify(string):
    identifier=string.split("_")[0]
    if(len(string.split("_"))>1):
        identifier=string.split("_")[0]+"_"+string.split("_")[1]
    return identifier
    
def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

#im.crop(vasak äär,ülemine äär,parem äär (piksleid vasakust äärest),alumine äär (piksleid ülemisest äärest))
for file in os.listdir(from_where):
    if(os.path.isfile(from_where+file)==False):
        continue
    print(file)
    identity=identify(file)
    identity=identity.replace('.png','')
    print(identity)
    im = Image.open(from_where+file)
    im_S1 = im.crop((0, 0, im.width/2, im.height))
    im_S2 = im.crop((im.width/2, 0, im.width, im.height))
    tile_coordinates_left=[]
    tile_coordinates_right=[]
    tile_coordinates_up=[]
    tile_coordinates_down=[]
    tiles_x=int(im_S1.width/tile_size)
    tiles_y=int(im_S1.height/tile_size)
    if(tiles_x<1 or tiles_y<1):
        continue
    for i in range(0,tiles_x):
        for j in range(0,tiles_y):
            im_tile_S1=im_S1.crop((i*tile_size,j*tile_size,tile_size*(i+1),tile_size*(j+1)))
            im_tile_S2=im_S2.crop((i*tile_size,j*tile_size,tile_size*(i+1),tile_size*(j+1)))
            get_concat_h(im_tile_S1, im_tile_S2).save(where_to+identity+'_'+str(i)+'_'+str(j)+'.png')
    if(im_S1.width>tiles_x*tile_size):
        for j in range(0,tiles_y):
            im_tile_S1=im_S1.crop((im_S1.width-tile_size,j*tile_size,im_S1.width,tile_size*(j+1)))
            im_tile_S2=im_S2.crop((im_S2.width-tile_size,j*tile_size,im_S2.width,tile_size*(j+1)))
            get_concat_h(im_tile_S1, im_tile_S2).save(where_to+identity+'_'+str(tiles_x)+'_'+str(j)+'.png')
    if(im_S1.height>tiles_y*tile_size):
        for i in range(0,tiles_x):
            im_tile_S1=im_S1.crop((i*tile_size,im_S1.height-tile_size,(i+1)*tile_size,im_S1.height))
            im_tile_S2=im_S2.crop((i*tile_size,im_S2.height-tile_size,(i+1)*tile_size,im_S2.height))
            get_concat_h(im_tile_S1, im_tile_S2).save(where_to+identity+'_'+str(i)+'_'+str(tiles_y)+'.png')
        if(im_S1.width>tiles_x*tile_size):
            im_tile_S1=im_S1.crop((im_S1.width-tile_size,im_S1.height-tile_size,im_S1.width,im_S1.height))
            im_tile_S2=im_S2.crop((im_S2.width-tile_size,im_S2.height-tile_size,im_S2.width,im_S2.height))
            get_concat_h(im_tile_S1, im_tile_S2).save(where_to+identity+'_'+str(tiles_x)+'_'+str(tiles_y)+'.png')
            
            
            
            
            
            
            
            
            
