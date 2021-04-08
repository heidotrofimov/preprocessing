import os
import datetime
import numpy as np
f=open('lines_for_gpt.txt','w')

S1=[]
S2=[]


for folder in os.listdir('s1_tif_final'):
    date_str=folder.split("_")[5].split("T")[0]
    year=int(date_str[0:4])
    month=int(date_str[4:6])
    day=int(date_str[6:8])
    date_S1=datetime.datetime(year,month,day)
    print(str(date_S1))
    days_between=2
    chosen_S2=""
    for folder2 in os.listdir('s2_zip'):
        date_str=folder2.split("_")[-1].split("T")[0]
        year=int(date_str[0:4])
        month=int(date_str[4:6])
        day=int(date_str[6:8])
        date_S2=datetime.datetime(year,month,day)
        days_between_tmp=np.abs((date_S2-date_S1).days)
        print("S2 date:"+str(date_S2))
        print("Days between: "+str(days_between_tmp))
        if(days_between_tmp<days_between):
            days_between=days_between_tmp
            chosen=folder2
    if(chosen_S2!=""):
        
        S1.append(folder)
        S2.append(chosen_S2)
print(S1)
print(S2)

'''
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
            
           
for S2_product in os.listdir('s2_zip'):
  for filename in os.listdir('s2_zip/'+S2_product+'/GRANULE/'):
    if("L2" in filename):
      if(os.path.exists('s2_zip/'+S2_product+"/GRANULE/output.dim")==False):
        line="/snap/snap8/bin/gpt Write -Ssource=s2_zip/"+S2_product+"/GRANULE/"+filename+"/ -Pfile=s2_zip/"+S2_product+"/GRANULE/output.dim"
        f.write(line+"\n")
        
f.close()
'''
