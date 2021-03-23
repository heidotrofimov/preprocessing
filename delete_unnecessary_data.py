import os
import shutil
import sys

if(sys.argv[1]=="before"):

    S2_dates=[]

    for folder in os.listdir('s2_zip'):
        S2_dates.append(folder.split("_")[2].split("T")[0])

    for folder in os.listdir('s1_zip'):
        date=folder.split("_")[4].split("T")[0]
        if(date not in S2_dates):
            shutil.rmtree('s1_zip/'+folder)
            
    for folder in os.listdir("s2_zip"):
        os.remove('s2_zip/'+folder+'/manifest.safe')
        for folder2 in os.listdir('s2_zip/'+folder+'/GRANULE/'):
            for filename in os.listdir('s2_zip/'+folder+'/GRANULE/'+folder2+'/IMG_DATA/R10m'):
                if("B02" not in filename and "B03" not in filename and "B04" not in filename and "B08" not in filename):
                    os.remove('s2_zip/'+folder+'/GRANULE/'+folder2+'/IMG_DATA/R10m/'+filename)
            shutil.rmtree('s2_zip/'+folder+'/GRANULE/'+folder2+'/IMG_DATA/R20m')
            shutil.rmtree('s2_zip/'+folder+'/GRANULE/'+folder2+'/IMG_DATA/R60m')
            
if(sys.argv[1]=="after"):
        
for folder in os.listdir('collocated'):
    if(".data" in folder):
        for filename in os.listdir('collocated/'+folder):
            if(os.path.isfile('collocated/'+folder+'/'+filename)):
                if("Amplitude" not in filename):
                    os.remove('collocated/'+folder+'/'+filename)
            else:
                shutil.rmtree('collocated/'+folder+'/'+filename)


