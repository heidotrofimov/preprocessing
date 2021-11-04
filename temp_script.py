import os

for product in os.listdir("checked_products"):
    for filename in os.listdir("checked_products/"+product):
        newname=filename.split("_")[-2]+"_"+filename.split("_")[-1]
        print(newname)
    
