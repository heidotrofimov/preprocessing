import os
import datetime
import numpy as np
f=open('lines_for_gpt.txt','w')

S1=[]
S2=[]
B02_list=[]
B02name_list=[]
targetpath_list=[]

def S1_name(S1_full):
    S1=S1_full.split(".")[0].split("_")
    return S1[0]+"_"+S1[4]+"_"+S1[-3]+"_"+S1[-2]+"_"+S1[-1]

def S2_name(S2_full):
    S2=S2_full.split(".")[0].split("_")
    return S2[0]+"_"+S2[2]+"_"+S2[5]

for S1_tif in os.listdir('s1_tif_final'):
    S1p='s1_tif_final/'+S1_tif
    date1=S1_tif.split("_")[5].split("T")[0]
    for S2_product in os.listdir("s2_zip"):
        date2=S2_product.split("_")[2].split("T")[0]
        if(date1==date2):
            
            name=S1_name(S1_tif)+"_colwith_"+S2_name(S2_product)
            for folder3 in os.listdir('s2_zip/'+S2_product+'/GRANULE/'):
                if("L2" in folder3):
                    for filename in os.listdir('s2_zip/'+S2_product+'/GRANULE/'+folder3+'/IMG_DATA/R10m/'):
                        if('B02_10m.jp2' in filename):
                            B02='/home/heido/projects/preprocessing/s2_zip/'+S2_product+'/GRANULE/'+folder3+'/IMG_DATA/R10m/'+filename
                            B02name=filename
            targetpath='/home/heido/projects/preprocessing/collocated/'+name+".dim"
            f.write("/snap/snap8/bin/gpt collocation.xml -PB02=\""+B02+"\" -PS1=\""+S1p+"\" -PB02name=\""+B02name+"\" -Ptargetpath=\""+targetpath+"\"\n")
            
                        
            
        
    
    '''
    year=int(date_str[0:4])
    month=int(date_str[4:6])
    day=int(date_str[6:8])
    date_S1=datetime.datetime(year,month,day)
    days_between=2
    chosen_S2=""
    B02=""
    B02name=""
    targetpath=""
    for folder2 in os.listdir('s2_zip'):
        date_str=folder2.split("_")[-1].split("T")[0]
        year=int(date_str[0:4])
        month=int(date_str[4:6])
        day=int(date_str[6:8])
        date_S2=datetime.datetime(year,month,day)
        days_between_tmp=np.abs((date_S2-date_S1).days)
        for folder3 in os.listdir('s2_zip/'+folder2+'/GRANULE/'):
            if("L2" in folder3):
                for filename in os.listdir('s2_zip/'+folder2+'/GRANULE/'+folder3+'/IMG_DATA/R10m/'):
                    if('B02_10m.jp2' in filename):
                        B02_tmp='/home/heido/projects/preprocessing/s2_zip/'+folder2+'/GRANULE/'+folder3+'/IMG_DATA/R10m/'+filename
                        B02name_tmp=filename
        targetpath_tmp='/home/heido/projects/preprocessing/collocated_2/'+folder.split(".")[0]+".dim"
        if(days_between_tmp<days_between):
            days_between=days_between_tmp
            chosen_S2=folder2
            B02=B02_tmp
            B02name=B02name_tmp
            targetpath=targetpath_tmp
    if(chosen_S2!=""):
        S1.append("/home/heido/projects/preprocessing/s1_tif_final_2/"+folder)
        S2.append(chosen_S2)
        B02_list.append(B02)
        B02name_list.append(B02name)
        targetpath_list.append(targetpath)
     '''   

'''        
for i in range(len(S1)):
    f.write("/snap/snap8/bin/gpt collocation.xml -PB02=\""+B02_list[i]+"\" -PS1=\""+S1[i]+"\" -PB02name=\""+B02name_list[i]+"\" -Ptargetpath=\""+targetpath_list[i]+"\"\n")
f.close()

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
