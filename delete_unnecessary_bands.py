import os
import shutil


for folder in os.listdir('collocated'):
    if(".data" in folder):
        for filename in os.listdir('collocated/'+folder):
            if(os.path.isfile('collocated/'+folder+'/'+filename)):
                if("Amplitude" not in filename):
                    os.remove('collocated/'+folder+'/'+filename)
            else:
                shutil.rmtree('collocated/'+folder+'/'+filename)


for folder in os.listdir("s2_zip"):
    os.remove('s2_zip/'+folder+'/manifest.safe')
    for folder2 in os.listdir('s2_zip/'+folder+'/GRANULE/'):
        for filename in os.listdir('s2_zip/'+folder+'/GRANULE/'+folder2+'/IMG_DATA/R10m'):
            if("B02" not in filename and "B03" not in filename and "B04" not in filename and "B08" not in filename):
                os.remove('s2_zip/'+folder+'/GRANULE/'+folder2+'/IMG_DATA/R10m/'+filename)
        shutil.rmtree('s2_zip/'+folder+'/GRANULE/'+folder2+'/IMG_DATA/R20m')
        shutil.rmtree('s2_zip/'+folder+'/GRANULE/'+folder2+'/IMG_DATA/R60m')
