import os
f=open('lines_for_gpt.txt','w')

for folder in os.listdir('s1_zip'):
    date=folder.split("_")[4].split("T")[0]
    for folder2 in os.listdir('s2_zip'):
        date2=folder2.split("_")[2].split("T")[0]
        if(date2==date):
            for folder3 in os.listdir('s2_zip/'+folder2+'/GRANULE/'):
                for filename in os.listdir('s2_zip/'+folder2+'/GRANULE/'+folder3+'/IMG_DATA/R10m/'):
                    if('B02_10m.jp2' in filename):
                        B02='/home/heido/projects/heido_test/s2_zip/'+folder2+'/GRANULE/'+folder3+'/IMG_DATA/R10m/'+filename
                        B02name=filename
            S1='/home/heido/projects/heido_test/s1_zip/'+folder+'/manifest.safe'
            targetpath='/home/heido/projects/heido_test/collocated/'+folder.split(".")[0]+".dim"
            f.write("/snap/snap8/bin/gpt collocation.xml -PB02=\""+B02+"\" -PS1=\""+S1+"\" -PB02name=\""+B02name+"\" -Ptargetpath=\""+targetpath+"\"\n")


f.close()
