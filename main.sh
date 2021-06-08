#!/bin/bash

/home/heido/miniconda3/envs/biomass/bin/python rename_tiffs.py

#delete unneccessary tifss in this step

sh ./linearize_rasters.sh s1_tif

sh ./combine_tiffs.sh s1_tif

python prepare_for_gpt.py

#Run collocation lines

python save_tifs.py

#Run the lines you get

python tif_tiler.py

#Before this file is run: download data to s2_zip, s1_zip

#python delete_unnecessary_data.py before

#python prepare_for_gpt.py

while IFS= read -r line; do
$line
done < lines_for_gpt.txt

#rm lines_for_gpt.txt

#python delete_unnecessary_data.py after

#python create_images.py


#After this file has run: delete cloudy tiles from S2_RGB_tiles, run "delete_cloudy_tiles.py" (will delete corresponding tiles from all other directories) and "add_history.py"

