import os

for filename in os.listdir("data/S1"):
  dt=os.path.getmtime("data/S1/"+filename)
  print(dt)
