import os


f2=open("missing.txt","w")

f= open("s2_data/products.dat","r")
lines = f.readlines()

missing=[]

for line in lines:
  olemas=False
  line2=line.rstrip()
  for filename in os.listdir("s2_data"):
    if(".SAFE" in filename):
      print(filename)
      if(line2==filename.split(".SAFE")[0]):
        print("Olen siin")
        olemas=True
  if(olemas==False):
    f2.write(line)
    missing.append(line)
    
f.close()
f2.close()

print(len(missing))
    
  
