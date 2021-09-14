import os
from datetime import datetime
from PIL import Image

history=[]

for S2 in os.listdir("data/S2"):
  histories=[]
  histories.append(S2)
  AOI=S2.split("_")[2]
  tile=S2.split(AOI+"_")[1]
  date_str=S2.split("_")[1].split("T")[0]
  date_obj=datetime(int(date_str[0:4]),int(date_str[4:6]),int(date_str[6:8]))
  for S2_2 in os.listdir("data/S2"):
      AOI2=S2_2.split("_")[2]
      tile2=S2_2.split(AOI2+"_")[1]
      date_str2=S2_2.split("_")[1].split("T")[0]
      date_obj2=datetime(int(date_str2[0:4]),int(date_str2[4:6]),int(date_str2[6:8]))
      if(AOI2==AOI and tile2==tile and date_obj2<date_obj and date_str2[0:4]==date_str[0:4]):
        histories.append(S2_2)
  if(len(histories)>1):
      history.append(histories)
  
history.sort(key=len)

for i in range(30):
  list_of_S2=history[-(i+1)]
  target=list_of_S2[0]
  AOI=target.split("_")[2]
  tile_nr=target.split(AOI+"_")[1]
  for S1 in os.listdir("data/S1"):
    corres_S2=S1.split("colwith_")[1].replace("tif","png")
    if(corres_S2==target):
      #os.system("cp data/S1/"+S1+" history_test/S1/")
      chosen_S1=S1
      break
  for h in list_of_S2[1:]:  
    S2_filename=target.split(AOI)[0]+AOI+"_"+h.split("_")[0]+"_"+h.split("_")[1]+"_"+tile_nr
    S1_filename=chosen_S1.split("_")[0]+"_"+chosen_S1.split("_")[1]+"_"+chosen_S1.split("_")[2]+"_colwith_"+S2_filename.replace("png","tif")
    os.system("cp data/S1/"+chosen_S1+" history_test/S1/"+S1_filename)
    target_im=Image.open("data/S2/"+target)
    history_im=Image.open("data/S2/"+h)
    dst = Image.new('RGB', (target_im.width + history_im.width, target_im.height))
    dst.paste(target_im, (0, 0))
    dst.paste(history_im, (target_im.width, 0))
    dst.save("history_test/S2/"+S2_filename)
    
  
