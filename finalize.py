import os

for s1_tile in os.listdir("s1_tiles_all"):
  tile="_"+s1_tile.split("_")[-2]+"_"+s1_tile.split("_")[-1].split(".")[0]
  s2=s1_tile.split("colwith_")[1].split(tile)[0]
  print(s1_tile)
  print(tile)
  print(s2)
