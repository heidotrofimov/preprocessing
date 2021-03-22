import os
import shutil

f=open("cloudless_tiles.txt","r")

for line in f.readlines():
  print(line.rstrip())
