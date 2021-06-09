import os


f2=open("missing.txt","r")

f= open("s2_data/products.dat")
lines = f.readlines()

for line in lines:
  olemas=False
  for filename in os.listdir("s2_data"):
    if(".SAFE" in filename):
      if(line==filename.split(".SAFE")[0]):
        olemas=True
  if(olemas==False):
    missing.write(line+"\n")
    
f.close()
f2.close()
    
  
